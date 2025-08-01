using Plots
using LaTeXStrings
using Printf

function forced_oscillator_system(y, ω₀, δ, γ, ω, t)
    x, x_dot = y
    forcing_term = γ * cos(ω * t)
    return [x_dot, forcing_term - δ * x_dot - ω₀^2 * x]
end

function rk4_step(f, y, h, ω₀, δ, γ, ω, t)
    k1 = h .* f(y,ω₀, δ, γ, ω, t)
    k2 = h .* f(y .+ 0.5 .* k1, ω₀, δ, γ, ω, t + 0.5 * h)
    k3 = h .* f(y .+ 0.5 .* k2, ω₀, δ, γ, ω, t + 0.5 * h)
    k4 = h .* f(y .+ k3, ω₀, δ, γ, ω, t + h)
    return y .+ (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4) ./ 6
end

function solve_forced_oscillator(ω₀, δ, γ, ω)
    x0, x0_dot = 0.0, 0.0
    t_max, h = 100.0, 0.01
    
    transient_steps = Int(floor(t_max / (2 * h)))

    y = [x0, x0_dot]
    t_vec, x_t, x_dot_t = Float64[], Float64[], Float64[]

    for (i, t) in enumerate(0:h:t_max)
        y = rk4_step(forced_oscillator_system, y, h, ω₀, δ, γ, ω, t)
        if i > transient_steps
            push!(t_vec, t)
            push!(x_t, y[1])
            push!(x_dot_t, y[2])
        end
    end
    
    return t_vec, x_t, x_dot_t
end

function main()
    theme(:wong2, frame_style=:box, grid=true, minorgrid=true)
    println("Generating plots for the underdamped, forced case...")

    ω₀ = 1.0
    δ = 0.5
    ω = 0.5
    gamma_values = [0.0, 1.0, 2.0, 3.0, 4.0]

    p_phase = plot(
        title = "Phase Space",
        xlabel = L"Position, $x(t)$",
        ylabel = L"Velocity, $\dot{x}(t)$",
        aspect_ratio = :equal,
        legend = false
    )

    p_time = plot(
        title = "Position vs. Time",
        xlabel = L"Time, $t$ (s)",
        ylabel = L"Position, $x(t)$",
        legend = :topright
    )

    for γ in gamma_values
        t_vec, x_t, x_dot_t = solve_forced_oscillator(ω₀, δ, γ, ω)
        plot!(p_phase, x_t, x_dot_t, linewidth=1.5)
        plot!(p_time, t_vec, x_t, linewidth=1.5, label = latexstring("\\gamma = $γ"))
    end
    
    combined_plot = plot(p_phase, p_time, 
                         layout = (1, 2), 
                         size=(1400, 600),
                         plot_title=" (δ=$δ) with Varying Driving Force",
                         left_margin = 10Plots.mm,
                         bottom_margin = 10Plots.mm)

    output_filename = "Damped_Forced_HO.png"
    savefig(combined_plot, output_filename)
    println("Saved plot to $output_filename")
    
    return combined_plot
end

main()
