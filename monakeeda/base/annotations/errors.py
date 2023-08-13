class NotAnAnnotationException(Exception):
    def __init__(self, annotation_cls):
        super(NotAnAnnotationException, self).__init__(
            f'{annotation_cls} is not a supported annotation -> implement it if needed and MAP it')
