// static/js/checkout.js
(() => {
    // Evita doble inicialización si el script se inyecta dos veces
    if (window.__checkoutInit) {
        console.warn("checkout.js ya estaba inicializado; se ignora la segunda carga.");
        return;
    }
    window.__checkoutInit = true;

    document.addEventListener("DOMContentLoaded", () => {
        console.log("✅ checkout.js cargado");

        // ---------------- Helpers ----------------
        function getCookie(name) {
            const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
            return m ? m.pop() : '';
        }

        // ---------------- Funcion de captura de errores pagos metamask ----------------
        function handleMetaMaskError(e) {
            console.log("🪵 Error completo (stringificado):", JSON.stringify(e, null, 2));

            const code = e?.info?.error?.code;
            const message = e?.info?.error?.message || e.message;

            if (code === 4001) {
                return "❌ Has cancelado la transacción desde MetaMask.";
            } else if (code === -32000) {
                return "❌ Fondos insuficientes en tu wallet.";
            } else if (code === -32002) {
                return "⚠️ Ya hay una transacción pendiente en MetaMask.";
            } else if (code === -32603) {
                return "⚠️ Error interno. Revisa tu wallet o intenta más tarde.";
            } else if (typeof message === "string") {
                return "❌ " + message;
            }

            return "❌ Error desconocido.";
        }


        const csrftoken = getCookie("csrftoken");

        const orderId = typeof window.orderId === "number" ? window.orderId : Number(window.orderId || 0);
        const baseTotal = parseFloat(String(window.orderTotal || 0)); // total de productos (backend)
        const urls = Object.assign({
            createQuote: "/orders/0/quote/",
            validatePayment: "/orders/validate-payment/",
            confirmPayment: "/orders/confirm_payment/",
            confirmPage: "/orders/confirm/",
        }, window.urls || {});

        // ---------------- DOM refs ----------------
        const shippingRadios = document.querySelectorAll("input[name='shipping']");
        const shippingCostEl = document.getElementById("shipping-cost");
        const subtotalEl = document.getElementById("subtotal");
        const taxEl = document.getElementById("tax");
        const totalEl = document.getElementById("total");

        const quoteBtn = document.getElementById("quoteBtn");
        const quoteBox = document.getElementById("quoteBox");

        const payBtn = document.getElementById("payBtn");
        const payOut = document.getElementById("payResult");

        // ---------------- Estado ----------------
        let currentTotal = 0;
        let quote = null; // { amount_crypto, symbol, receiving_address, expires_at, ... }
        let countdownInterval = null;
        let isQuoting = false;
        let isPaying = false;
        let txInFlightHash = null;

        // ---------------- Totales ----------------
        function updateTotals() {
            const checked = document.querySelector("input[name='shipping']:checked");
            const shippingCost = checked ? parseFloat(checked.dataset.cost) : 0;

            const subtotal = baseTotal + shippingCost;
            const tax = subtotal * 0.21; // IVA demo
            const total = subtotal + tax;

            shippingCostEl.textContent = "€" + shippingCost.toFixed(2);
            subtotalEl.textContent = "€" + subtotal.toFixed(2);
            taxEl.textContent = "€" + tax.toFixed(2);
            totalEl.textContent = "€" + total.toFixed(2);

            currentTotal = +total.toFixed(2);
        }

        shippingRadios.forEach(r => r.addEventListener("change", updateTotals));
        updateTotals();

        // ---------------- Utils ----------------
        async function postJSON(url, data) {
            const res = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify(data || {}),
            });
            const json = await res.json().catch(() => ({}));
            return {ok: res.ok && json && json.ok, json, status: res.status};
        }

        function startCountdown(seconds) {
            clearInterval(countdownInterval);
            let left = seconds;
            countdownInterval = setInterval(() => {
                if (!quote) {
                    clearInterval(countdownInterval);
                    return;
                }
                if (left <= 0) {
                    clearInterval(countdownInterval);
                    quoteBox.textContent = "❌ Cotización expirada, vuelve a obtenerla.";
                    if (payBtn) payBtn.disabled = true;
                    quote = null;
                    return;
                }
                quoteBox.textContent = `💰 ${quote.amount_crypto} ${quote.symbol} · ⏳ ${left}s`;
                left--;
            }, 1000);
        }

        function quoteExpired(q) {
            if (!q || !q.expires_at) return true;
            const expiresMs = Date.parse(q.expires_at);
            return Number.isFinite(expiresMs) ? Date.now() >= expiresMs : false;
        }

        // ---------------- Obtener cotización (ETH) ----------------
        if (quoteBtn) {
            quoteBtn.addEventListener("click", async () => {
                if (isQuoting) return; // single-flight
                isQuoting = true;

                if (!orderId) {
                    quoteBox.textContent = "⚠️ orderId no disponible.";
                    isQuoting = false;
                    return;
                }

                quoteBtn.disabled = true;
                quoteBox.textContent = "⏳ Obteniendo cotización…";

                try {
                    // 1) Validación demo (backend simplemente dice OK)
                    const v = await postJSON(urls.validatePayment, {order_id: orderId, total: currentTotal});
                    if (!v.ok) {
                        quoteBox.textContent = "⚠️ Error validando el total.";
                        return;
                    }

                    // 2) Crear cotización en backend (usa el order_id en la URL)
                    const q = await postJSON(urls.createQuote, {amount_eur: currentTotal});
                    if (!q.ok) {
                        quoteBox.textContent = "⚠️ Error obteniendo cotización.";
                        return;
                    }

                    quote = q.json; // { ok:true, amount_crypto, symbol, receiving_address, expires_at, ... }
                    if (payBtn) payBtn.disabled = false;
                    startCountdown(180);
                } catch (e) {
                    quoteBox.textContent = "⚠️ Error de red: " + (e.message || e);
                } finally {
                    quoteBtn.disabled = false;
                    isQuoting = false;
                }
            });
        }

        // ---------------- Pagar con MetaMask ----------------
        if (payBtn) {
            payBtn.addEventListener("click", async () => {
                if (isPaying) return; // ya hay una tx en curso
                if (!orderId) {
                    payOut.textContent = "⚠️ orderId no disponible.";
                    return;
                }
                if (!quote || quoteExpired(quote)) {
                    payOut.textContent = "⚠️ Cotización no válida o expirada.";
                    return;
                }

                isPaying = true;
                payBtn.disabled = true;
                payOut.textContent = "⏳ Verificando…";

                try {
                    const v = await postJSON(urls.validatePayment, {order_id: orderId, total: currentTotal});
                    if (!v.ok) throw new Error("Validación fallida en el backend.");

                    if (!window.ethereum) throw new Error("MetaMask no detectado.");

                    const SEPOLIA = "0xaa36a7";
                    await window.ethereum.request({method: "eth_requestAccounts"});
                    const chainId = await window.ethereum.request({method: "eth_chainId"});
                    if (chainId !== SEPOLIA) {
                        await window.ethereum.request({
                            method: "wallet_switchEthereumChain",
                            params: [{chainId: SEPOLIA}],
                        });
                    }

                    const provider = new ethers.BrowserProvider(window.ethereum);
                    const signer = await provider.getSigner();

                    if (txInFlightHash) {
                        payOut.textContent = "⏳ Transacción pendiente: " + txInFlightHash;
                        return;
                    }

                    const tx = await signer.sendTransaction({
                        to: quote.receiving_address,
                        value: ethers.parseEther(String(quote.amount_crypto)),
                    });

                    txInFlightHash = tx.hash;
                    payOut.innerHTML = `
  <div style="max-width: 100%; padding: 0.5em 1em; background: #f8f9fa; border-radius: 8px; font-size: 0.9em;">
    <p>🚀 Transacción registrada. Esperando la TX:</p>
    <p style="overflow-x: auto; white-space: nowrap; font-family: monospace; margin: 0;">
      <code id="txHash" style="cursor: pointer; user-select: all;">${tx.hash}</code>
    </p>
    <p id="copyNotice" style="display:none; color: green; font-size: 0.8em; margin-top: 4px;">✅ Copiado al portapapeles</p>
  </div>
`;

                    // Evento para copiar al portapapeles
                    document.getElementById("txHash").addEventListener("click", () => {
                        const txEl = document.getElementById("txHash");
                        const txHash = txEl.textContent;

                        navigator.clipboard.writeText(txHash).then(() => {
                            const notice = document.getElementById("copyNotice");
                            if (notice) {
                                notice.style.display = "inline";
                                setTimeout(() => (notice.style.display = "none"), 2000);
                            }
                        });
                    });


                    // Esperar confirmación del backend
                    const maxWaitMs = 90_000;
                    const stepMs = 3_000;
                    let elapsed = 0;
                    let confirmed = false;

                    while (elapsed < maxWaitMs) {
                        const r = await postJSON(urls.confirmPayment, {order_id: orderId, txHash: tx.hash});
                        if (r.ok) {
                            confirmed = true;
                            break;
                        }
                        if (r.json && r.json.pending) {
                            await new Promise(res => setTimeout(res, stepMs));
                            elapsed += stepMs;
                            continue;
                        }
                        throw new Error(r.json && r.json.error ? r.json.error : "Error en la verificación.");
                    }

                    if (confirmed) {
                        const confirmUrl = urls.confirmPage || "/orders/confirm/";
                        const url = `${confirmUrl}?id=${encodeURIComponent(orderId)}&tx=${encodeURIComponent(tx.hash)}`;
                        window.location.href = url;
                    } else {
                        payOut.textContent = `⏱️ La transacción no fue confirmada todavía. TX: ${tx.hash}`;
                    }

                } catch (e) {
                    payOut.textContent = handleMetaMaskError(e);
                    payOut.classList.remove("text-muted", "text-success");
                    payOut.classList.add("text-danger");

                } finally {
                    // Permitimos reintentar SOLO si no se ha redirigido
                    isPaying = false;
                    payBtn.disabled = false;
                }
            });
        }
        // ---------------- Stripe (opcional): validar antes de enviar ----------------
        const stripeForm = document.querySelector("form[action*='stripe_checkout']");
        if (stripeForm) {
            stripeForm.addEventListener("submit", async (e) => {
                e.preventDefault();

                // Validar el total con el backend
                const v = await postJSON(urls.validatePayment, {
                    order_id: orderId,
                    total: currentTotal
                });

                if (!v.ok) {
                    alert("❌ Error validando: " + (v.json?.error || "desconocido"));
                    return;
                }

                // Añadir campo oculto con el total
                let hidden = stripeForm.querySelector("input[name='amount']");
                if (!hidden) {
                    hidden = document.createElement("input");
                    hidden.type = "hidden";
                    hidden.name = "amount";
                    stripeForm.appendChild(hidden);
                }
                hidden.value = currentTotal;

                // Enviar formulario
                stripeForm.submit();
            });
        }


    });
})();
