constraint_collisions_validation = {
    ('lt', 'gt'): lambda x, y: x - 1 > y,
    ('lt', 'lte'): lambda x, y: x - 1 == y,
    ('lt', 'gte'): lambda x, y: x > y,
    ('lt', 'lt'): lambda x, y: x == y,
    ('gt', 'lte'): lambda x, y: x < y,
    ('gt', 'gte'): lambda x, y: x + 1 == y,
    ('gt', 'gt'): lambda x, y: x == y,
    ('lte', 'gte'): lambda x, y: x >= y,
    ('lte', 'lte'): lambda x, y: x == y,
    ('gte', 'gte'): lambda x, y: x == y
}
