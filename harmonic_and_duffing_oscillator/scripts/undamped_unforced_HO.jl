using Plots
using LaTeXStrings
using Printf


function undamped_oscillator_system(y, ω₀)
    x, x_dot = y
    return [x_dot, -ω₀^2 * x]
end


function rk4_step(f, y, h, ω₀)
    k1 = h .* f(y, ω₀)
    k2 = h .* f(y .+ 0.5 .* k1, ω₀)
    k3 = h .* f(y .+ 0.5 .* k2, ω₀)
    k4 = h .* f(y .+ k3, ω₀)
    return y .+ (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4) ./ 6
end


function generate_undamped_plot(ω₀)
    initial_conditions = [
        (2.0, 0.0), (0.0, 2.0), (1.5, 1.5), (-1.0, 1.0), (0.5, -1.0)
    ]
    T = 2π / ω₀
    t_max, h = T, 0.01

    p = plot(
        title = latexstring("\\omega_0 = $ω₀"),
        xlabel = L"Position, $x(t)$", ylabel = L"Velocity, $\dot{x}(t)$",
        aspect_ratio = :equal, legend = :topright,
        titlefontsize = 14, legendfontsize = 7
    )

    for (x0, x0_dot) in initial_conditions
        y = [x0, x0_dot]
        x_t, x_dot_t = [y[1]], [y[2]]
        

        for t in 0:h:t_max
            y = rk4_step(undamped_oscillator_system, y, h, ω₀)
            push!(x_t, y[1])
            push!(x_dot_t, y[2])
        end
        
        
        label_str = latexstring(Printf.format(
            Printf.Format(L"(x_0, \dot{x}_0) = (%.1f, %.1f), T \approx %.2fs"),
            x0, x0_dot, T
        ))
        plot!(p, x_t, x_dot_t, linewidth=1.5, label=label_str)
    end
    return p
end


function main()
    
    theme(:wong2, frame_style=:box, grid=true, minorgrid=true)

    println("Generating plots for the undamped case...")


    plot_omega_1 = generate_undamped_plot(1.0)
    plot_omega_2 = generate_undamped_plot(2.0)

 
    final_layout = plot(plot_omega_1, plot_omega_2,
                        layout = (1, 2),
                        size = (1800, 700))

    savefig(final_layout, "UD-UF_HO.png")
    println("Saved plot to UD-UF_HO.png")
    
    return final_layout
end


main()

