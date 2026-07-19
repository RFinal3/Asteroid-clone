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


def point_in_polygon(point, polygon_points):
    inside = False

    for index in range(len(polygon_points)):
        edge_start = polygon_points[index]
        next_index = (index + 1) % len(polygon_points)
        edge_end = polygon_points[next_index]
        edge_crosses_y = (edge_start.y > point.y) != (edge_end.y > point.y)

        if edge_crosses_y:
            vertical_distance = edge_end.y - edge_start.y
            distance_to_ray = point.y - edge_start.y
            fraction_along_edge = distance_to_ray / vertical_distance
            intersection_x = edge_start.x + (
                edge_end.x - edge_start.x
            ) * fraction_along_edge

            if intersection_x > point.x:
                inside = not inside

    return inside


def polygons_collide(polygon_a, polygon_b):
    for index_a in range(len(polygon_a)):
        edge_a_start = polygon_a[index_a]
        next_a_index = (index_a + 1) % len(polygon_a)
        edge_a_end = polygon_a[next_a_index]
        
        for index_b in range(len(polygon_b)):
            edge_b_start = polygon_b[index_b]
            next_b_index = (index_b + 1) % len(polygon_b)
            edge_b_end = polygon_b[next_b_index]
            
            if line_segments_intersect(edge_a_start, edge_a_end, edge_b_start, edge_b_end):
                return True

    if point_in_polygon(polygon_a[0], polygon_b):
        return True

    if point_in_polygon(polygon_b[0], polygon_a):
        return True

    return False


def line_segments_intersect(a_start, a_end, b_start, b_end):
    a_vector = a_end - a_start
    b_vector = b_end - b_start
    a_to_b = b_start - a_start
    denominator = a_vector.cross(b_vector)

    if abs(denominator) < 0.000001:
        return False

    a_proportion = a_to_b.cross(b_vector) / denominator
    b_proportion = a_to_b.cross(a_vector) / denominator

    return (
    0 <= a_proportion <= 1
    and 0 <= b_proportion <= 1
    )


def circle_collides_with_polygon(circle_center, circle_radius, polygon_points):
    for index in range(len(polygon_points)):
        edge_start = polygon_points[index]
        next_index = (index + 1) % len(polygon_points)
        edge_end = polygon_points[next_index]
        edge_vector = edge_end - edge_start
        start_to_circle = circle_center - edge_start
        edge_length_squared = edge_vector.length_squared()
        projection = start_to_circle.dot(edge_vector) / edge_length_squared
        projection = max(0.0, min(1.0, projection))
        closest_point = edge_start + edge_vector * projection
        distance = closest_point.distance_to(circle_center)

        if distance <= circle_radius:
            return True

    return point_in_polygon(circle_center, polygon_points)