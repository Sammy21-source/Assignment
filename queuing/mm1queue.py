def analyze_mm1_queue(lam: float, mu: float) -> dict:
    """
    Calculates core M/M/1 queue metrics.
    lam = Arrival rate (lambda)
    mu  = Service rate (mu)
    """
    rho = lam / mu
    
    # The system is only stable if the service rate is greater than the arrival rate
    if rho >= 1:
        return {"error": "System is unstable: Arrival rate must be less than service rate."}

    # Core M/M/1 Formulas
    p0 = 1 - rho           # Probability the server is idle
    ls = rho / (1 - rho)   # Expected number of customers in the system
    lq = ls - rho          # Expected number of customers in the queue
    ws = ls / lam          # Expected time a customer spends in the system
    wq = lq / lam          # Expected time a customer spends waiting in the queue

    return {
        "Traffic Intensity (rho)": rho,
        "Probability Idle (P0)": p0,
        "Avg in System (Ls)": ls,
        "Avg in Queue (Lq)": lq,
        "Time in System (Ws)": ws,
        "Time in Queue (Wq)": wq
    }

if __name__ == "__main__":
    # Example parameters
    LAMBDA = 8.0  # Arrival rate
    MU = 9.0      # Service rate

    print(f"--- M/M/1 Queue Analysis (λ={LAMBDA}, μ={MU}) ---")
    
    results = analyze_mm1_queue(LAMBDA, MU)
    
    if "error" in results:
        print(results["error"])
    else:
        for metric, value in results.items():
            print(f"{metric:<25}: {value:.4f}")
