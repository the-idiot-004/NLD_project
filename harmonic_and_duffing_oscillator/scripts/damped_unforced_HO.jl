using Plots
using LaTeXStrings

theme(:wong2, frame_style=:box, grid=true, minorgrid=true)

function oscillator_system(y, ω₀, δ_coeff)
    x, x_dot = y
    dx_dt = x_dot
    dx_dot_dt = -δ_coeff * x_dot - ω₀^2 * x
    return [dx_dt, dx_dot_dt]
end

function rk4_step(f, y, h, ω₀, δ_coeff)
    k1 = h .* f(y, ω₀, δ_coeff)
    k2 = h .* f(y .+ 0.5 .* k1, ω₀, δ_coeff)
    k3 = h .* f(y .+ 0.5 .* k2, ω₀, δ_coeff)
    k4 = h .* f(y .+ k3, ω₀, δ_coeff)
    return y .+ (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4) ./ 6
end

function generate_damped_plot(ω₀, δ_coeff, title_str)
    initial_conditions = [
        (3.0, 0.0),
        (-2.5, 2.5),
        (0.0, -4.0),
        (2.0, 4.0),
        (-1.0, -3.0)
    ]
    t_max = 25.0 
    h = 0.01

    p = plot(
        title = title_str,
        xlabel = L"Position, $x(t)$",
        ylabel = L"Velocity, $\dot{x}(t)$",
        aspect_ratio = :equal,
        legend = false
    )

    for (x0, x0_dot) in initial_conditions
        x_t = Float64[]
        x_dot_t = Float64[]
        y = [x0, x0_dot]
        
        for t in 0:h:t_max
            push!(x_t, y[1])
            push!(x_dot_t, y[2])
            y = rk4_step(oscillator_system, y, h, ω₀, δ_coeff)
        end
        
        plot!(p, x_t, x_dot_t, linewidth=1.5, label=nothing)
    end
    return p
end

omega_0_base = 1.0

delta_under = 0.5 
plot_under = generate_damped_plot(omega_0_base, delta_under, "Underdamped (δ=$delta_under)")

delta_crit = 2.0 * omega_0_base
plot_crit = generate_damped_plot(omega_0_base, delta_crit, "Critically Damped (δ=$delta_crit)")

delta_over = 4.0
plot_over = generate_damped_plot(omega_0_base, delta_over, "Overdamped (δ=$delta_over)")

final_layout = plot(plot_under, plot_crit, plot_over,
                    layout = (1, 3),
                    size = (1800, 600)
                   )

savefig(final_layout, "D-UF_HO.png")

final_layout
