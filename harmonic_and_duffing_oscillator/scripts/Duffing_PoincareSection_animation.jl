using Plots
using LaTeXStrings

# --- ODE System and Solver ---

function duffing_forced_system(y, δ, β, α, γ, ω, t)
    x, x_dot = y
    forcing_term = γ * cos(ω * t)
    return [x_dot, forcing_term - δ * x_dot - β * x - α * x^3]
end

function rk4_step(f, y, h, δ, β, α, γ, ω, t)
    k1 = h .* f(y,            δ, β, α, γ, ω, t)
    k2 = h .* f(y .+ 0.5 .* k1, δ, β, α, γ, ω, t + 0.5 * h)
    k3 = h .* f(y .+ 0.5 .* k2, δ, β, α, γ, ω, t + 0.5 * h)
    k4 = h .* f(y .+ k3,        δ, β, α, γ, ω, t + h)
    return y .+ (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4) ./ 6
end

# --- Animation Function ---

function main()
    theme(:wong2)
    println("Generating Poincaré section animation...")

    # System parameters
    δ = 0.5
    ω = 1.0
    β = -1.0
    α = 1.0
    
    # Bifurcation parameter range for γ
    gamma_range = 0.3:0.001:0.4
    
    # Simulation parameters
    h = 0.01
    T = 2π / ω
    transient_periods = 200 # Number of periods to discard
    collection_periods = 500 # Number of periods to sample

    # Create the animation object
    anim = @animate for γ in gamma_range
        
        y = [0.0, 0.0] # Start from the same initial condition each time
        
        # Evolve through transient periods
        for t_step in 1:round(Int, transient_periods * T / h)
            t = t_step * h
            y = rk4_step(duffing_forced_system, y, h, δ, β, α, γ, ω, t)
        end

        # Evolve and collect Poincaré section points
        poincare_x = Float64[]
        poincare_y = Float64[]
        for t_step in 1:round(Int, collection_periods * T / h)
            t = (transient_periods * T) + (t_step * h)
            y = rk4_step(duffing_forced_system, y, h, δ, β, α, γ, ω, t)
            
            # Check if we are at a multiple of the driving period
            if abs(rem(t, T)) < h/2
                push!(poincare_x, y[1])
                push!(poincare_y, y[2])
            end
        end
        
        # Plot the collected points for the current γ value
        scatter(poincare_x, poincare_y,
                marker = (:circle, 2),
                markerstrokewidth = 0,
                alpha = 0.7,
                legend = false,
                title = latexstring("\\gamma = $(round(γ, digits=4))"),
                xlabel = L"$x(nT)$",
                ylabel = L"$\dot{x}(nT)$",
                xlims = (-2, 2),
                ylims = (-1.5, 1.5)
        )
    end

    # Save the GIF
    output_filename = "Duffing_Poincare_Animation.gif"
    gif(anim, output_filename, fps = 15)
    println("Saved animation to $output_filename")
    
    return anim
end

main()
