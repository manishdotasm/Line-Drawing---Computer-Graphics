import glfw
from OpenGL.GL import *



def draw_grid(window_width, window_height):
    glColor3f(0.5, 0.5, 0.5)  # Set color to gray
    glBegin(GL_LINES)

    # Draw vertical lines
    for i in range(-window_width // 2, window_width // 2 + 1, 10):
        glVertex2f(i, -window_height // 2)
        glVertex2f(i, window_height // 2)

    # Draw horizontal lines
    for j in range(-window_height // 2, window_height // 2 + 1, 10):
        glVertex2f(-window_width // 2, j)
        glVertex2f(window_width // 2, j)

    glEnd()


# DDA Algorithm 
def DDA(point1, point2):
    glColor3f(1, 0, 0)
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    nsteps = max(abs(dx), abs(dy))

    if nsteps == 0:
        glBegin(GL_POINTS)
        glVertex2f(point1[0], point1[1])
        glEnd()
    else:
        x_inc = dx / nsteps
        y_inc = dy / nsteps
        x = point1[0]
        y = point1[1]

        glBegin(GL_POINTS)
        for _ in range(nsteps):
            glVertex2f(x, y)
            x += x_inc
            y += y_inc 
        glEnd()


def bresenham(point1, point2):
    glColor3f(0, 0, 1)
    x1, y1 = point1
    x2, y2 = point2
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    glBegin(GL_POINTS)
    while (x1 != x2) or (y1 != y2):
        glVertex2f(x1, y1)
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    glEnd()

# histogram drawer
def histogram(points, choice):
    # 0 = dda, 1 = bresenham
    size = len(points)
    if (choice == 0):
        for i in range(size-1):
            DDA(points[i], points[i+1])
        return
    
    if (choice == 1):
        for i in range(size-1):
            bresenham(points[i], points[i+1])
        return
        
    print("ERROR!")







def main():
    if not glfw.init():
        print("GLFW could not be initiated.")
        return

    window_width, window_height = 800, 600
    window = glfw.create_window(window_width, window_height, "Line Drawing", None, None)
    if not window:
        glfw.terminate()
        return
        
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # Setting up the view
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width, height = glfw.get_framebuffer_size(window)
        glOrtho(-width / 2, width / 2, -height / 2, height / 2, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        draw_grid(window_height, window_width)

        #DDA((0, 0), (150, 100))
        #bresenham((0,0), (100, 150))


        data = [(50, 100), (100, 70), (150, 120), (200, 110), (250, 140)]
        points = [(50, 70), (100, 40), (150, 90), (200, 80), (250, 110)]

        histogram(data, 1)
        histogram(points, 0)


        

        # Highlight center
        glPointSize(2)
        glColor3f(1.0, 0.0, 0.0)  # Set color to red
        glBegin(GL_POINTS)
        glVertex2f(0, 0)  # Draw a point at the center
        glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
