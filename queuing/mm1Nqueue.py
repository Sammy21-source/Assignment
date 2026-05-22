def analyze_mm1n_queue(lam: float, mu: float, N: int) -> dict:
    """
    Calculates core metrics for an M/M/1:N queue (finite capacity).
    lam = Arrival rate (lambda)
    mu  = Service rate (mu)
    N   = Maximum system capacity (queue + server)
    """
    rho = lam / mu
    
    # Handle the math depending on whether traffic intensity is exactly 1
    if abs(rho - 1.0) < 1e-10:
        p0 = 1.0 / (N + 1)
        ls = N / 2.0
    else:
        p0 = (1.0 - rho) / (1.0 - rho ** (N + 1))
        num = rho * (1 + N * rho**(N+1) - (N+1) * rho**N)
        den = (1 - rho) * (1 - rho**(N+1))
        ls = num / den

    # Probability the system is full (customers are turned away)
    pn = (rho ** N) * p0
    
    # Effective arrival rate (only customers who aren't blocked actually join)
    lambda_eff = lam * (1.0 - pn)
    
    # Core M/M/1:N Formulas (Little's Law)
    lq = ls - (lambda_eff / mu)          # Expected customers in the queue
    ws = ls / lambda_eff if lambda_eff > 0 else 0  # Expected time in the system
    wq = ws - (1.0 / mu)                 # Expected time in the queue

    return {
        "Traffic Intensity (rho)": rho,
        "Probability Idle (P0)": p0,
        "Probability Full/Blocked (Pn)": pn,
        "Effective Arrival Rate (λ_eff)": lambda_eff,
        "Avg in System (Ls)": ls,
        "Avg in Queue (Lq)": lq,
        "Time in System (Ws)": ws,
        "Time in Queue (Wq)": wq
    }


if __name__ == "__main__":
    # Example parameters
    LAMBDA = 8.0  # Arrival rate
    MU = 9.0      # Service rate
    N = 10        # Maximum system capacity

    print(f"--- M/M/1:N Queue Analysis (λ={LAMBDA}, μ={MU}, N={N}) ---")
    
    # Note: Unlike the standard M/M/1 queue, a finite queue is stable 
    # even if arrival rate > service rate (rho >= 1) because excess 
    # arrivals are simply turned away.
    results = analyze_mm1n_queue(LAMBDA, MU, N)
    
    for metric, value in results.items():
        print(f"{metric:<30}: {value:.4f}")