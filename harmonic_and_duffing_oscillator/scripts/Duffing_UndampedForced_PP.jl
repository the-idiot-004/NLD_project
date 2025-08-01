using Plots
using LaTeXStrings

function duffing_damped_system(y, δ)
    x, x_dot = y
    return [x_dot, x - x^3 - δ * x_dot]
end

function rk4_step(f, y, h, δ)
    k1 = h .* f(y, δ)
    k2 = h .* f(y .+ 0.5 .* k1, δ)
    k3 = h .* f(y .+ 0.5 .* k2, δ)
    k4 = h .* f(y .+ k3, δ)
    return y .+ (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4) ./ 6
end

function main()
    theme(:wong2, frame_style=:box, grid=true, minorgrid=true)
    println("Generating phase portrait for the damped Duffing oscillator...")

    δ = 0.5

    initial_conditions = [
        (0.5, 0.0), (1.8, 0.0), (0.0, 1.0),
        (-0.5, 0.0), (-1.8, 0.0), (0.0, -1.0)
    ]
    
    t_max, h = 40.0, 0.01

    p = plot(
        title = "Phase Portrait of the Damped Duffing Oscillator (δ=$δ)",
        xlabel = L"Position, $x(t)$",
        ylabel = L"Velocity, $\dot{x}(t)$",
        aspect_ratio = :equal,
        legend = false,
        xlims = (-2.5, 2.5),
        ylims = (-1.5, 1.5)
    )

    scatter!(p, [1, -1], [0, 0], marker=:circle, color=:black, markersize=5)
    scatter!(p, [0], [0], marker=:xcross, color=:red, markersize=6)

    for (x0, v0) in initial_conditions
        y = [x0, v0]
        x_t, x_dot_t = [y[1]], [y[2]]
        
        for t_val in h:h:t_max
            y = rk4_step(duffing_damped_system, y, h, δ)
            push!(x_t, y[1])
            push!(x_dot_t, y[2])
        end
        
        plot!(p, x_t, x_dot_t, linewidth=1.0)
    end
    
    output_filename = "Duffing_Damped_Phase_Portrait.png"
    savefig(p, output_filename)
    println("Saved plot to $output_filename")
    
    return p
end

main()

