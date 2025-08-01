using Plots
using LaTeXStrings

function duffing_forced_system(y, δ, β, α, γ, ω, t)
    x, x_dot = y
    forcing_term = γ * cos(ω * t)
    return [x_dot, forcing_term - δ * x_dot - β * x - α * x^3]
end

function rk4_step(f, y, h, δ, β, α, γ, ω, t)
    k1 = h .* f(y,δ, β, α, γ, ω, t)
    k2 = h .* f(y .+ 0.5 .* k1, δ, β, α, γ, ω, t + 0.5 * h)
    k3 = h .* f(y .+ 0.5 .* k2, δ, β, α, γ, ω, t + 0.5 * h)
    k4 = h .* f(y .+ k3,δ, β, α, γ, ω, t + h)
    return y .+ (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4) ./ 6
end

function generate_attractor_plot(δ, β, α, γ, ω)
    x0, v0 = 0.0, 0.0
    t_max, h = 1000.0, 0.01
    
    # Time after which we start plotting to ignore transients
    t_transient = 200.0

    p = plot(
        title = latexstring("\\gamma = $γ"),
        aspect_ratio = :equal,
        legend = false,
        framestyle = :box,
        xlims = (-2, 2),
        ylims = (-1.5, 1.5)
    )

    y = [x0, v0]
    x_t, x_dot_t = Float64[], Float64[]

    for t in 0:h:t_max
        y = rk4_step(duffing_forced_system, y, h, δ, β, α, γ, ω, t)
        if t > t_transient
            push!(x_t, y[1])
            push!(x_dot_t, y[2])
        end
    end
    
    plot!(p, x_t, x_dot_t, linewidth=0.5, alpha=0.8)
    return p
end

function main()
    theme(:wong2)

    # Parameters from problem statement (d)
    δ = 0.5
    ω = 1.0
    β = -1.0
    α = 1.0
    gamma_values = [0.33, 0.35, 0.357, 0.365]

    plots_array = []
    for γ in gamma_values
        push!(plots_array, generate_attractor_plot(δ, β, α, γ, ω))
    end
    
    final_layout = plot(plots_array...,
                        layout = (2, 2),
                        size = (1200, 1000),
                        plot_title = "Period-Doubling Route to Chaos in the Duffing Oscillator",
                        left_margin=5Plots.mm, bottom_margin=5Plots.mm)

    output_filename = "Duffing_Period_Doubling.png"
    savefig(final_layout, output_filename)
    println("Saved plot to $output_filename")
    
    return final_layout
end

main()
