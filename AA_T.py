import pygame, pymunk, pymunk.pygame_util

def apple(space, pos):
    body = pymunk.Body(10, 10, body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    body.angular_velocity = -10
    shape = pymunk.Circle(body, 20)
    shape.collision_type = 1
    shape.elasticity = 1
    space.add(body, shape)
    return body, shape

def ledge(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)    
    shape = pymunk.Segment(body, (600,400), (0, 500), 2)
    shape.collision_type = 0
    shape.elasticity = 0.5
    space.add(body, shape)
    return shape

def post_solve_arrow_hit(arbiter, space, data):
    a, b = arbiter.shapes
    position = arbiter.contact_point_set.points[0].point_a
    print(position)
    ledge_body = a.body
    ball_body = b.body
    pivot_joint = pymunk.PivotJoint(ball_body, ledge_body, position)
    space.add(pivot_joint)

pygame.init()
clock=pygame.time.Clock()

screen = pygame.display.set_mode((600,500))
space = pymunk.Space()
space.gravity = (50 ,700)


apples = []
ledge_shape = ledge(space)

handler = space.add_collision_handler(0, 1)
handler.data["apples"] = apples
handler.post_solve = post_solve_arrow_hit

while True:    
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONUP:
            ball_body, arrow_shape = apple(space, event.pos)
            apples.append(arrow_shape)
            
    space.debug_draw(pymunk.pygame_util.DrawOptions(screen))
    
    space.step(1/60)
    pygame.display.update()
    clock.tick(60)