using Plots
using LaTeXStrings
using ProgressMeter
using Base.Threads

# --- system parameters ---
struct DuffingParameters
    δ::Float64
    β::Float64
    α::Float64
    γ::Float64
    ω::Float64
end

function duffing_forced_system(y, p::DuffingParameters, t)
    x, x_dot = y
    forcing_term = p.γ * cos(p.ω * t)
    return [x_dot, forcing_term - p.δ * x_dot - p.β * x - p.α * x^3]
end

function rk4_step(f, y, h, p::DuffingParameters, t)
    k1 = h .* f(y,p, t)
    k2 = h .* f(y .+ 0.5 .* k1, p, t + 0.5 * h)
    k3 = h .* f(y .+ 0.5 .* k2, p, t + 0.5 * h)
    k4 = h .* f(y .+ k3, p, t + h)
    return y .+ (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4) ./ 6
end

# --- Main Basin of Attraction Function ---

function main()
    theme(:wong2, frame_style=:box, grid=true)
    p = DuffingParameters(0.3, -1.0, 1.0, 0.3, 1.2)

    # Simulation parameters
    num_periods = 100
    T = 2π / p.ω
    tf = num_periods * T
    h = 0.02
    
    # Grid resolution
    resolution = 400
    x_range = range(-2, 2, length=resolution)
    v_range = range(-2, 2, length=resolution)

    basin_matrix = zeros(Int, resolution, resolution)

    println("Calculating fractal basin boundary on $(nthreads()) threads...")
    prog = Progress(resolution, 1, "Integrating rows...")

    # Using multithreading to parallelize the outer loop
    @threads for i in 1:resolution
        x0 = x_range[i]
        for (j, v0) in enumerate(v_range)
            y = [x0, v0]
            for t in 0:h:tf
                y = rk4_step(duffing_forced_system, y, h, p, t)
            end
            # Classify the final state based on its x-position
            basin_matrix[j, i] = (y[1] > 0) ? 1 : 2
        end
        next!(prog)
    end
    println("\nCalculation complete. Plotting...")

    #plot
    plt = heatmap(
        x_range,
        v_range,
        basin_matrix,
        c = cgrad([:dodgerblue, :orangered]),
        title = "Fractal Basin Boundary of the Duffing Oscillator",
        xlabel = "Initial Position, x(0)",
        ylabel = "Initial Velocity, v(0)",
        legend = false,
        colorbar = false,
        aspect_ratio = :equal,
        size = (800, 800)
    )

    output_filename = "Duffing_Fractal_Basin_Boundary.png"
    savefig(plt, output_filename)
    println("Saved plot to $output_filename")
    
    return plt
end

main()

