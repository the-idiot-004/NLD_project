using Plots
using LaTeXStrings
using ProgressMeter

function duffing_forced_system(y, δ, β, α, γ, ω, t)
    x, x_dot = y
    forcing_term = γ * cos(ω * t)
    return [x_dot, forcing_term - δ * x_dot - β * x - α * x^3]
end

function rk4_step(f, y, h, δ, β, α, γ, ω, t)
    k1 = h .* f(y, δ, β, α, γ, ω, t)
    k2 = h .* f(y .+ 0.5 .* k1, δ, β, α, γ, ω, t + 0.5 * h)
    k3 = h .* f(y .+ 0.5 .* k2, δ, β, α, γ, ω, t + 0.5 * h)
    k4 = h .* f(y .+ k3, δ, β, α, γ, ω, t + h)
    return y .+ (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4) ./ 6
end

function main()
    theme(:default)

    δ = 0.5
    ω = 1.0
    β = -1.0
    α = 1.0
    gamma_range = 0.33:0.0001:0.4
    
    h = 0.01
    T = 2π / ω
    transient_periods = 50 
    collection_periods = 500

    bifurcation_gamma = Float64[]
    bifurcation_x = Float64[]

    println("Generating optimized bifurcation diagram...")
    prog = Progress(length(gamma_range), 1, "Sweeping γ...")

    y = [0.0, 0.0] 

    for γ in gamma_range
        for t_step in 1:round(Int, transient_periods * T / h)
            t = t_step * h
            y = rk4_step(duffing_forced_system, y, h, δ, β, α, γ, ω, t)
        end

        # Collect Poincaré points, using the final 'y' from the previous step
        for t_step in 1:round(Int, collection_periods * T / h)
            t = (transient_periods * T) + (t_step * h)
            y = rk4_step(duffing_forced_system, y, h, δ, β, α, γ, ω, t)
            
            if abs(rem(t, T)) < h/2
                push!(bifurcation_gamma, γ)
                push!(bifurcation_x, y[1])
            end
        end
        next!(prog)
    end
    println("\nCalculation complete. Plotting...")

    p = scatter(
        bifurcation_gamma,
        bifurcation_x,
        marker = (:circle, 1, 0.1, :black),
        markerstrokewidth = 0,
        legend = false,
        grid = false,
        framestyle = :box,
        xlabel = L" $\gamma$",
        ylabel = L"$x$"
    )

    output_filename = "Duffing_Bifurcation_Diagram.png"
    savefig(p, output_filename)
    println("Saved plot to $output_filename")
    
    return p
end

main()
