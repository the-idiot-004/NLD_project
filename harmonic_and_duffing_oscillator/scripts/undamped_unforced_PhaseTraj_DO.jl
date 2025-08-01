using Plots
using LaTeXStrings
using Printf

function duffing_conservative_system(y)
    x, x_dot = y
    return [x_dot, x - x^3]
end

function rk4_step(f, y, h)
    k1 = h .* f(y)
    k2 = h .* f(y .+ 0.5 .* k1)
    k3 = h .* f(y .+ 0.5 .* k2)
    k4 = h .* f(y .+ k3)
    return y .+ (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4) ./ 6
end

function solve_and_get_period(x0, v0, t_max, h)
    y = [x0, v0]
    t_vec, x_t, x_dot_t = [0.0], [y[1]], [y[2]]
    peak_times = Float64[]

    for t_val in h:h:t_max
        y_prev = y
        y = rk4_step(duffing_conservative_system, y, h)
        push!(t_vec, t_val)
        push!(x_t, y[1])
        push!(x_dot_t, y[2])

        if y_prev[2] > 0 && y[2] <= 0 && length(peak_times) < 2
            push!(peak_times, t_val)
        end
    end
    
    T_numerical = 0.0
    if length(peak_times) == 2
        T_numerical = 2 * (peak_times[2] - peak_times[1])
    end

    return t_vec, x_t, x_dot_t, T_numerical
end

function main()
    theme(:wong2, frame_style=:box, grid=true, minorgrid=true)

    initial_conditions = [
        (0.3, 0.0), (1.0, 1.0), (-0.5, -0.5), (0.0, 0.1),
        (0.0, 0.0001), (-0.5, 0.0), (-1.0, 0.3), (1.0, 0.3),
        (-2.0, -1.0), (-0.1, -0.1), (0.2, 0.2)
    ]
    
    t_max, h = 60.0, 0.01

    # ---Phase Portrait Plot ---
    p_phase = plot(
        title = L"Phase Portrait $(\delta=0, \gamma=0, \beta=-1, \alpha=1)$",
        xlabel = L"Position, $x(t)$",
        ylabel = L"Velocity, $\dot{x}(t)$",
        aspect_ratio = :equal,
        legend = :topleft,
        legendfontsize=7,
        size=(1000, 800)
    )

    # --- Time Series Plot ---
    p_time = plot(
        title = L"Position vs. Time $(\delta=0, \gamma=0, \beta=-1, \alpha=1)$",
        xlabel = L"Time, $t$ (s)",
        ylabel = L"Position, $x(t)$",
        legend = :outertopright,
        size=(1000, 800),
        legendfontsize=7
    )

    for (x0, v0) in initial_conditions
        t_vec, x_t, x_dot_t, T_numerical = solve_and_get_period(x0, v0, t_max, h)
        
        label_str = @sprintf("x0=%.4g, v0=%.4g, T=%.4f", x0, v0, T_numerical)
        
        plot!(p_phase, x_t, x_dot_t, linewidth=1.5, label=label_str)
        plot!(p_time, t_vec, x_t, linewidth=1.0, label=label_str)
    end
    
    # --- Save the plots  ---
    phase_filename = "Duffing_UndampedUnforced_PP.png"
    time_filename = "Duffing_UndampedUnforced_Time_Series.png"
    
    savefig(p_phase, phase_filename)
    println("Saved phase portrait to $phase_filename")
    
    savefig(p_time, time_filename)
    println("Saved time series plot to $time_filename")
    
    
    return p_phase
end

main()

