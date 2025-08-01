using Plots
gr()  # Ensure GR backend


"Returns dx/dt and dv/dt for the oscillator system"
function oscillator_system(y, ω₀, δ)
    x, v = y
    return [v, -δ * v - ω₀^2 * x]
end

"Performs a single RK4 integration step"
function rk4_step(f, y, h, ω₀, δ)
    k1 = h .* f(y, ω₀, δ)
    k2 = h .* f(y .+ 0.5 .* k1, ω₀, δ)
    k3 = h .* f(y .+ 0.5 .* k2, ω₀, δ)
    k4 = h .* f(y .+ k3, ω₀, δ)
    return y .+ (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4) ./ 6
end

"Solves the oscillator for position over time using RK4"
function solve_for_position(ω₀, δ, x0, v0, t_max, h)
    x_t, t_array = Float64[], Float64[]
    y = [x0, v0]
    for t in 0:h:t_max
        push!(x_t, y[1])
        push!(t_array, t)
        y = rk4_step(oscillator_system, y, h, ω₀, δ)
    end
    return t_array, x_t
end

# --- Spring Drawing  ---

"Generates zig-zag points for the spring"
function spring_points(start_x, end_x; segments=20, amp=0.2)
    xs, ys = [start_x], [0.0]
    seg_len = (end_x - start_x) / segments
    for i in 1:segments-1
        push!(xs, start_x + i * seg_len)
        push!(ys, amp * (-1)^i)
    end
    push!(xs, end_x)
    push!(ys, 0.0)
    return xs, ys
end

# --- Animation Plotting ---

"Creates and saves the animation for a given damping value"
function animate_spring_system(δ; ω₀=1.0, x0=3.0, v0=0.0, t_max=20.0, h=0.02, name="demo")
    t_arr, x_arr = solve_for_position(ω₀, δ, x0, v0, t_max, h)
    total_frames = length(t_arr)

    println("Generating animation for δ = $δ ...")

    anim = @animate for i in 1:total_frames
        pos = x_arr[i]
        time_now = t_arr[i]

        p1 = plot(framestyle=:none, xlims=(-x0-1, x0+1), ylims=(-1.2, 1.2), aspect_ratio=:equal)
        
        # Wall and reference line       
        plot!([-x0-0.5, -x0-0.5], [-1, 1], color=:black, linewidth=3)
        plot!([0, 0], [-1, 1], color=:gray, linestyle=:dash)
        
        # Spring
        xs, ys = spring_points(-x0-0.5, pos)
        plot!(xs, ys, color=:black, linewidth=1.5)
        
        # Mass
        scatter!([pos], [0.0], markersize=18, markercolor=:steelblue, markerstrokecolor=:black)

        p2 = plot(t_arr, x_arr, label="x(t)", xlabel="Time", ylabel="Position",
                  xlims=(0, t_max), ylims=(-x0, x0))
                  
        # Time pointer line
        vline!([time_now], color=:gray, linestyle=:dash, label="")
        
        # Vertical line from block to its time series point
        scatter!([time_now], [pos], color=:red, label="Current", markersize=6)

        plot(p1, p2, layout=(1, 2), size=(900, 400), title="Damping δ = $δ   Time = $(round(time_now, digits=2))s")
    end

    gif(anim, "$name.gif", fps=30)
    println("Saved $name.gif")
end

# --- Run ---

animate_spring_system(0.5, name="underdamped")          # Underdamped
animate_spring_system(2.0, name="critically_damped")    # Critically damped
animate_spring_system(4.0, name="overdamped")           # Overdamped

