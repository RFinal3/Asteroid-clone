from constants import SCREEN_HEIGHT, SCREEN_WIDTH

def wrap_position(position, radius):
    if position.x > SCREEN_WIDTH + radius:
        position.x = -radius

    elif position.x < -radius:
        position.x = SCREEN_WIDTH + radius

    if position.y > SCREEN_HEIGHT + radius:
        position.y = -radius
        
    elif position.y < -radius:
        position.y = SCREEN_HEIGHT + radius


def circle_collides_with_triangle(circle_center, circle_radius, triangle_points):
    cross_products = []

    for index in range(len(triangle_points)):
        edge_start = triangle_points[index]
        next_index = (index + 1) % len(triangle_points)
        edge_end = triangle_points[next_index]
        edge_vector = edge_end - edge_start
        start_to_circle = circle_center - edge_start
        cross_product = edge_vector.cross(start_to_circle)
        cross_products.append(cross_product)
        edge_length_squared = edge_vector.length_squared()
        projection = start_to_circle.dot(edge_vector) / edge_length_squared
        projection = max(0.0, min(1.0, projection))
        closest_point = edge_start + edge_vector * projection
        distance = closest_point.distance_to(circle_center)

        if distance <= circle_radius:
            return True

    all_positive = all(value >= 0 for value in cross_products)
    all_negative = all(value <= 0 for value in cross_products)

    return all_positive or all_negative