"""Decision-making agent using Google Gemini API directly (not via OpenRouter)."""

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import json
import logging
from datetime import datetime
from src.backend.config_loader import CONFIG
from src.backend.indicators.taapi_client import TAAPIClient
import requests


class GeminiTradingAgent:
    """Trading agent powered by Google Gemini API with function calling support."""

    def __init__(self):
        """Initialize Gemini configuration and indicator helper."""
        self.api_key = CONFIG["gemini_api_key"]
        self.model_name = CONFIG["gemini_model"]
        self.taapi = TAAPIClient()

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in configuration")

        # Configure Gemini SDK
        genai.configure(api_key=self.api_key)

        # Initialize model with safety settings
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )

        logging.info(f"Initialized GeminiTradingAgent with model: {self.model_name}")

    def decide_trade(self, assets, context):
        """Decide for multiple assets in one call.

        Args:
            assets: Iterable of asset tickers to score.
            context: Structured market/account state forwarded to Gemini.

        Returns:
            List of trade decision payloads, one per asset.
        """
        return self._decide(context, assets=assets)

    def _decide(self, context, assets):
        """Dispatch decision request to Gemini and enforce output contract."""
        system_prompt = (
            "You are a rigorous QUANTITATIVE TRADER and interdisciplinary MATHEMATICIAN-ENGINEER optimizing risk-adjusted returns for perpetual futures under real execution, margin, and funding constraints.\n"
            "You will receive market + account context for SEVERAL assets, including:\n"
            f"- assets = {json.dumps(assets)}\n"
            "- per-asset intraday (5m) and higher-timeframe (4h) metrics\n"
            "- Active Trades with Exit Plans\n"
            "- Recent Trading History\n\n"
            "Always use the 'current time' provided in the user message to evaluate any time-based conditions, such as cooldown expirations or timed exit plans.\n\n"
            "Your goal: make decisive, first-principles decisions per asset that minimize churn while capturing edge.\n\n"
            "Aggressively pursue setups where calculated risk is outweighed by expected edge; size positions so downside is controlled while upside remains meaningful.\n\n"
            "Core policy (low-churn, position-aware)\n"
            "1) Respect prior plans: If an active trade has an exit_plan with explicit invalidation (e.g., \"close if 4h close above EMA50\"), DO NOT close or flip early unless that invalidation (or a stronger one) has occurred.\n"
            "2) Hysteresis: Require stronger evidence to CHANGE a decision than to keep it. Only flip direction if BOTH:\n"
            "   a) Higher-timeframe structure supports the new direction (e.g., 4h EMA20 vs EMA50 and/or MACD regime), AND\n"
            "   b) Intraday structure confirms with a decisive break beyond ~0.5×ATR (recent) and momentum alignment (MACD or RSI slope).\n"
            "   Otherwise, prefer HOLD or adjust TP/SL.\n"
            "3) Cooldown: After opening, adding, reducing, or flipping, impose a self-cooldown of at least 3 bars of the decision timeframe (e.g., 3×5m = 15m) before another direction change, unless a hard invalidation occurs. Encode this in exit_plan (e.g., \"cooldown_bars:3 until 2025-10-19T15:55Z\"). You must honor your own cooldowns on future cycles.\n"
            "4) Funding is a tilt, not a trigger: Do NOT open/close/flip solely due to funding unless expected funding over your intended holding horizon meaningfully exceeds expected edge (e.g., > ~0.25×ATR). Consider that funding accrues discretely and slowly relative to 5m bars.\n"
            "5) Overbought/oversold ≠ reversal by itself: Treat RSI extremes as risk-of-pullback. You need structure + momentum confirmation to bet against trend. Prefer tightening stops or taking partial profits over instant flips.\n"
            "6) Prefer adjustments over exits: If the thesis weakens but is not invalidated, first consider: tighten stop (e.g., to a recent swing or ATR multiple), trail TP, or reduce size. Flip only on hard invalidation + fresh confluence.\n\n"
            "Decision discipline (per asset)\n"
            "- Choose one: buy / sell / hold.\n"
            "- Proactively harvest profits when price action presents a clear, high-quality opportunity that aligns with your thesis.\n"
            "- You control allocation_usd.\n"
            "- TP/SL sanity:\n"
            "  • BUY: tp_price > current_price, sl_price < current_price\n"
            "  • SELL: tp_price < current_price, sl_price > current_price\n"
            "  If sensible TP/SL cannot be set, use null and explain the logic.\n"
            "- exit_plan must include at least ONE explicit invalidation trigger and may include cooldown guidance you will follow later.\n\n"
            "Leverage policy (perpetual futures)\n"
            "- YOU CAN USE LEVERAGE, ATLEAST 3X LEVERAGE TO GET BETTER RETURN, KEEP IT WITHIN 10X IN TOTAL\n"
            "- In high volatility (elevated ATR) or during funding spikes, reduce or avoid leverage.\n"
            "- Treat allocation_usd as notional exposure; keep it consistent with safe leverage and available margin.\n\n"
            "Tool usage\n"
            "- Aggressively leverage fetch_taapi_indicator whenever an additional datapoint could sharpen your thesis; keep parameters minimal (indicator, symbol like \"BTC/USDT\", interval \"5m\"/\"4h\", optional period).\n"
            "- Incorporate tool findings into your reasoning, but NEVER paste raw tool responses into the final JSON—summarize the insight instead.\n"
            "- Use tools to upgrade your analysis; lack of confidence is a cue to query them before deciding.\n"
            "Reasoning recipe (first principles)\n"
            "- Structure (trend, EMAs slope/cross, HH/HL vs LH/LL), Momentum (MACD regime, RSI slope), Liquidity/volatility (ATR, volume), Positioning tilt (funding, OI).\n"
            "- Favor alignment across 4h and 5m. Counter-trend scalps require stronger intraday confirmation and tighter risk.\n\n"
            "Output contract\n"
            "- Output a STRICT JSON object with exactly two properties in this order:\n"
            "  • reasoning: detailed but concise string (max 4000 chars) capturing key analysis. Do not write a novel.\n"
            "  • trade_decisions: array ordered to match the provided assets list.\n"
            "- Each item inside trade_decisions must contain the keys {asset, action, allocation_usd, tp_price, sl_price, exit_plan, rationale}.\n"
            "- Do not emit Markdown or any extra properties.\n"
        )

        # Define function/tool for TAAPI indicator fetching
        fetch_taapi_tool = genai.protos.Tool(
            function_declarations=[
                genai.protos.FunctionDeclaration(
                    name="fetch_taapi_indicator",
                    description=(
                        "Fetch any TAAPI indicator. Available: ema, sma, rsi, macd, bbands, stochastic, stochrsi, "
                        "adx, atr, cci, dmi, ichimoku, supertrend, vwap, obv, mfi, willr, roc, mom, sar (parabolic), "
                        "fibonacci, pivotpoints, keltner, donchian, awesome, gator, alligator, and 200+ more. "
                        "See https://taapi.io/indicators/ for full list and parameters."
                    ),
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            "indicator": genai.protos.Schema(type=genai.protos.Type.STRING),
                            "symbol": genai.protos.Schema(type=genai.protos.Type.STRING),
                            "interval": genai.protos.Schema(type=genai.protos.Type.STRING),
                            "period": genai.protos.Schema(type=genai.protos.Type.INTEGER),
                            "backtrack": genai.protos.Schema(type=genai.protos.Type.INTEGER),
                            "other_params": genai.protos.Schema(
                                type=genai.protos.Type.OBJECT,
                                properties={}
                            ),
                        },
                        required=["indicator", "symbol", "interval"]
                    )
                )
            ]
        )

        # Build JSON schema for structured output
        schema = self._build_schema(assets)

        # Configure generation with JSON mode
        generation_config = genai.types.GenerationConfig(
            response_mime_type="application/json",
            response_schema=schema,
            temperature=0.7,
            max_output_tokens=8192,
        )

        # Log the request
        logging.info(f"Sending request to Gemini (model: {self.model_name})")
        with open("llm_requests.log", "a", encoding="utf-8") as f:
            f.write(f"\n\n=== {datetime.now()} ===\n")
            f.write(f"Model: {self.model_name}\n")
            f.write(f"Provider: Google Gemini (Direct API)\n")
            f.write(f"Context length: {len(context)} characters\n")

        # Create chat session with tools
        chat = self.model.start_chat(
            history=[],
            enable_automatic_function_calling=False,
            # tools=[fetch_taapi_tool] # Temporarily disabled to fix unhashable type error
        )

        # Send initial message with system prompt + context
        full_prompt = f"{system_prompt}\n\n{context}"
        
        logging.info(f"Sending prompt to Gemini (Length: {len(full_prompt)})")

        try:
            # First turn: Send the prompt
            response = chat.send_message(
                full_prompt,
                generation_config=generation_config
            )

            max_turns = 10
            for turn in range(max_turns):
                # Check if model wants to use functions from the LAST response
                part = response.candidates[0].content.parts[0]
                
                if part.function_call:
                    function_call = part.function_call
                    
                    if function_call.name == "fetch_taapi_indicator":
                        # Execute the function call
                        args = dict(function_call.args)
                        logging.info(f"Gemini requested TAAPI indicator: {args}")

                        try:
                            params = {
                                "secret": self.taapi.api_key,
                                "exchange": "binance",
                                "symbol": args["symbol"],
                                "interval": args["interval"],
                            }
                            if args.get("period") is not None:
                                params["period"] = args["period"]
                            if args.get("backtrack") is not None:
                                params["backtrack"] = args["backtrack"]
                            if args.get("other_params") and isinstance(args["other_params"], dict):
                                params.update(args["other_params"])

                            ind_resp = requests.get(
                                f"{self.taapi.base_url}{args['indicator']}",
                                params=params,
                                timeout=30
                            ).json()
                            
                            function_result = {"result": ind_resp}

                        except Exception as ex:
                            function_result = {"error": str(ex)}

                        # Send function response back to Gemini
                        # This generates the NEXT response from the model
                        response = chat.send_message(
                            genai.protos.Content(
                                parts=[
                                    genai.protos.Part(
                                        function_response=genai.protos.FunctionResponse(
                                            name="fetch_taapi_indicator",
                                            response=function_result
                                        )
                                    )
                                ]
                            ),
                            generation_config=generation_config,
                        )
                        continue  # Process the new response in the next iteration

                # If no function call, we have the final text response
                break
            
            # --- Processing the Final Response ---
            response_text = response.text
            logging.info(f"Gemini response received ({len(response_text)} chars)")

            with open("llm_requests.log", "a", encoding="utf-8") as f:
                f.write(f"Response:\n{response_text[:500]}...\n")

            # Parse JSON response
            try:
                parsed = json.loads(response_text)
            except json.JSONDecodeError as e:
                logging.error(f"JSON parse error: {e}")
                # Fallback: try to extract JSON from markdown code blocks
                if "```json" in response_text:
                    start = response_text.find("```json") + 7
                    end = response_text.find("```", start)
                    if end > start:
                        try:
                            parsed = json.loads(response_text[start:end].strip())
                        except json.JSONDecodeError:
                            parsed = None
                else:
                    parsed = None

            if not isinstance(parsed, dict):
                logging.error("Expected dict payload from Gemini")
                return self._fallback_response(assets)

            reasoning_text = parsed.get("reasoning", "") or ""
            decisions = parsed.get("trade_decisions")

            if isinstance(decisions, list):
                normalized = []
                for item in decisions:
                    if isinstance(item, dict):
                        item.setdefault("allocation_usd", 0.0)
                        item.setdefault("tp_price", None)
                        item.setdefault("sl_price", None)
                        item.setdefault("exit_plan", "")
                        item.setdefault("rationale", "")
                        normalized.append(item)
                return {"reasoning": reasoning_text, "trade_decisions": normalized}

            logging.error("trade_decisions missing or invalid")
            return self._fallback_response(assets, reasoning=reasoning_text)

        except Exception as e:
            logging.error(f"Gemini API error: {e}", exc_info=True)
            return self._fallback_response(assets)

    def _build_schema(self, assets):
        """Build JSON schema for Gemini's structured output."""
        return {
            "type": "object",
            "properties": {
                "reasoning": {"type": "string"},
                "trade_decisions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "asset": {"type": "string", "enum": assets},
                            "action": {"type": "string", "enum": ["buy", "sell", "hold"]},
                            "allocation_usd": {"type": "number"},
                            "tp_price": {"type": "number"},
                            "sl_price": {"type": "number"},
                            "exit_plan": {"type": "string"},
                            "rationale": {"type": "string"},
                        },
                        "required": ["asset", "action", "allocation_usd", "exit_plan", "rationale"]
                    }
                }
            },
            "required": ["reasoning", "trade_decisions"]
        }

    def _fallback_response(self, assets, reasoning="Error occurred"):
        """Generate fallback HOLD response when API fails."""
        return {
            "reasoning": reasoning,
            "trade_decisions": [{
                "asset": a,
                "action": "hold",
                "allocation_usd": 0.0,
                "tp_price": None,
                "sl_price": None,
                "exit_plan": "",
                "rationale": "API error - defaulting to HOLD"
            } for a in assets]
        }
