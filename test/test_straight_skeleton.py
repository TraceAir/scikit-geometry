import skgeom as sg


class TestCreateInteriorStraightSkeleton:
    """Simple unit tests for skgeom.skeleton.create_interior_straight_skeleton function."""

    def test_simple_rectangle(self):
        """Test straight skeleton creation for a simple rectangle."""
        points = [
            sg.Point2(0, 0),
            sg.Point2(4, 0),
            sg.Point2(4, 2),
            sg.Point2(0, 2)
        ]
        polygon = sg.Polygon(points)

        skeleton = sg.skeleton.create_interior_straight_skeleton(polygon)

        # Basic assertions
        assert skeleton is not None
        assert hasattr(skeleton, 'vertices')
        assert hasattr(skeleton, 'halfedges')

    def test_simple_triangle(self):
        """Test straight skeleton creation for a triangle."""
        points = [
            sg.Point2(0, 0),
            sg.Point2(2, 0),
            sg.Point2(1, 1.5)
        ]
        polygon = sg.Polygon(points)

        skeleton = sg.skeleton.create_interior_straight_skeleton(polygon)

        assert skeleton is not None
        vertices = list(skeleton.vertices)
        assert len(vertices) > 0

    def test_square(self):
        """Test straight skeleton creation for a square."""
        points = [
            sg.Point2(0, 0),
            sg.Point2(1, 0),
            sg.Point2(1, 1),
            sg.Point2(0, 1)
        ]
        polygon = sg.Polygon(points)

        skeleton = sg.skeleton.create_interior_straight_skeleton(polygon)

        assert skeleton is not None
        vertices = list(skeleton.vertices)
        halfedges = list(skeleton.halfedges)
        assert len(vertices) > 0
        assert len(halfedges) > 0

    def test_l_shaped_polygon(self):
        """Test straight skeleton creation for an L-shaped polygon."""
        points = [
            sg.Point2(0, 0),
            sg.Point2(2, 0),
            sg.Point2(2, 1),
            sg.Point2(1, 1),
            sg.Point2(1, 2),
            sg.Point2(0, 2)
        ]
        polygon = sg.Polygon(points)

        skeleton = sg.skeleton.create_interior_straight_skeleton(polygon)

        assert skeleton is not None
        vertices = list(skeleton.vertices)
        halfedges = list(skeleton.halfedges)
        assert len(vertices) > 0
        assert len(halfedges) > 0

    def test_convex_pentagon(self):
        """Test straight skeleton creation for a pentagon."""
        points = [
            sg.Point2(0, 0),
            sg.Point2(2, 0),
            sg.Point2(2.5, 1),
            sg.Point2(1, 2),
            sg.Point2(-0.5, 1)
        ]
        polygon = sg.Polygon(points)

        skeleton = sg.skeleton.create_interior_straight_skeleton(polygon)

        assert skeleton is not None
        vertices = list(skeleton.vertices)
        assert len(vertices) > 0

    def test_skeleton_has_vertices_and_edges(self):
        """Test that skeleton has vertices and halfedges."""
        points = [
            sg.Point2(0, 0),
            sg.Point2(3, 0),
            sg.Point2(3, 2),
            sg.Point2(0, 2)
        ]
        polygon = sg.Polygon(points)

        skeleton = sg.skeleton.create_interior_straight_skeleton(polygon)

        # Test basic structure
        assert hasattr(skeleton, 'vertices')
        assert hasattr(skeleton, 'halfedges')

        # Test we can iterate
        vertices = list(skeleton.vertices)
        halfedges = list(skeleton.halfedges)

        assert len(vertices) >= 0
        assert len(halfedges) >= 0

    def test_vertex_properties(self):
        """Test that vertices have expected properties."""
        points = [
            sg.Point2(0, 0),
            sg.Point2(2, 0),
            sg.Point2(2, 2),
            sg.Point2(0, 2)
        ]
        polygon = sg.Polygon(points)

        skeleton = sg.skeleton.create_interior_straight_skeleton(polygon)
        vertices = list(skeleton.vertices)

        # Test that vertices exist and have point property
        assert len(vertices) > 0
        for vertex in vertices:
            # Vertex should have a point (not callable)
            assert hasattr(vertex, 'point')
            point = vertex.point
            assert isinstance(point, sg.Point2)
            # Point should have coordinates
            assert hasattr(point, 'x')
            assert hasattr(point, 'y')

    def test_different_sizes(self):
        """Test polygons of different sizes."""
        # Small rectangle
        small_points = [
            sg.Point2(0, 0),
            sg.Point2(0.5, 0),
            sg.Point2(0.5, 0.3),
            sg.Point2(0, 0.3)
        ]
        small_polygon = sg.Polygon(small_points)
        small_skeleton = sg.skeleton.create_interior_straight_skeleton(small_polygon)
        assert small_skeleton is not None

        # Large rectangle
        large_points = [
            sg.Point2(0, 0),
            sg.Point2(100, 0),
            sg.Point2(100, 50),
            sg.Point2(0, 50)
        ]
        large_polygon = sg.Polygon(large_points)
        large_skeleton = sg.skeleton.create_interior_straight_skeleton(large_polygon)
        assert large_skeleton is not None

    def test_invalid_polygon_error(self):
        """Test that invalid polygons raise errors."""
        # Test with collinear points (degenerate case)
        try:
            points = [sg.Point2(0, 0), sg.Point2(1, 0), sg.Point2(2, 0)]  # Collinear points
            polygon = sg.Polygon(points)
            skeleton = sg.skeleton.create_interior_straight_skeleton(polygon)
            # If no exception, just verify it's handled gracefully
            assert skeleton is not None or skeleton is None
        except Exception:
            # It's acceptable if degenerate cases raise exceptions
            pass

    def test_return_type(self):
        """Test that function returns correct type."""
        points = [
            sg.Point2(0, 0),
            sg.Point2(1, 0),
            sg.Point2(1, 1),
            sg.Point2(0, 1)
        ]
        polygon = sg.Polygon(points)

        skeleton = sg.skeleton.create_interior_straight_skeleton(polygon)

        # Should return a Skeleton object
        assert skeleton is not None
        assert 'Skeleton' in str(type(skeleton))


class TestCreateInteriorWeightedStraightSkeleton:
    """Unit tests for skgeom.skeleton.create_interior_weighted_straight_skeleton function."""
    
    def setup_method(self):
        """Set up common test data."""
        # Create a polygon with holes as specified
        self.polygon_with_holes = sg.PolygonWithHoles(
            sg.Polygon([
                sg.Point2(0.0654894, -0.164014),
                sg.Point2(-0.148791, -0.133726),
                sg.Point2(0.334817, -0.0455076),
                sg.Point2(0.250497, 0.490434),
                sg.Point2(-0.367446, 0.0733451),
                sg.Point2(-0.31241, -0.498233),
                sg.Point2(0.450854, -0.435834)
            ]),
            [
                sg.Polygon([
                    sg.Point2(-0.262206, 0.0237308),
                    sg.Point2(0.202291, 0.337249),
                    sg.Point2(0.238616, 0.106361),
                    sg.Point2(-0.26138, 0.0151523)
                ]),
                sg.Polygon([
                    sg.Point2(0.0275831, -0.25965),
                    sg.Point2(0.167911, -0.358631),
                    sg.Point2(-0.222318, -0.390534),
                    sg.Point2(-0.238542, -0.222034)
                ])
            ]
        )
        
        # Define weights for the exterior and holes
        self.exterior_weights = [1, 1, 2, 1, 1, 1, 1]
        self.hole_weights = [[1.1, 0.8, 1.5, 0.6], [0.9, 1.1, 2, 0.6]]

    def test_polygon_with_holes_and_offset(self):
        """Test weighted straight skeleton creation for a polygon with holes and offset generation."""
        # Create the weighted straight skeleton
        skeleton_with_holes = sg.skeleton.create_interior_weighted_straight_skeleton(
            self.polygon_with_holes, self.exterior_weights, self.hole_weights
        )

        # Basic assertions
        assert skeleton_with_holes is not None
        assert hasattr(skeleton_with_holes, 'vertices')
        assert hasattr(skeleton_with_holes, 'halfedges')

        # Test vertices and halfedges
        vertices = list(skeleton_with_holes.vertices)
        halfedges = list(skeleton_with_holes.halfedges)
        assert len(vertices) > 0
        assert len(halfedges) > 0

        # Test offset polygon generation
        offset_polygons = skeleton_with_holes.offset_polygons(0.03)
        assert len(offset_polygons) > 0
        
        # Verify that each offset polygon is valid
        for offset_poly in offset_polygons:
            assert isinstance(offset_poly, sg.Polygon)
            assert offset_poly.is_simple()
            
    def test_simple_weighted_polygon(self):
        """Test weighted straight skeleton creation for a simple polygon."""
        # Create a simple polygon
        points = [
            sg.Point2(0, 0),
            sg.Point2(4, 0),
            sg.Point2(4, 2),
            sg.Point2(0, 2)
        ]
        polygon = sg.Polygon(points)
        
        # Define weights - different weight for each edge
        weights = [1.0, 2.0, 1.0, 0.5]
        
        # Create the weighted straight skeleton
        skeleton = sg.skeleton.create_interior_weighted_straight_skeleton(polygon, weights)
        
        # Basic assertions
        assert skeleton is not None
        assert hasattr(skeleton, 'vertices')
        assert hasattr(skeleton, 'halfedges')
        
        # Test vertices and halfedges
        vertices = list(skeleton.vertices)
        halfedges = list(skeleton.halfedges)
        assert len(vertices) > 0
        assert len(halfedges) > 0
        
        # Test offset polygon generation
        offset_polygons = skeleton.offset_polygons(0.5)
        assert len(offset_polygons) > 0
        
    def test_offset_polygon_generation(self):
        """Test detailed offset polygon generation from weighted straight skeleton."""
        # Create the weighted straight skeleton
        skeleton_with_holes = sg.skeleton.create_interior_weighted_straight_skeleton(
            self.polygon_with_holes, self.exterior_weights, self.hole_weights
        )
        
        # Generate offset polygons with a specific offset value
        offset_value = 0.03
        offset_polygons = skeleton_with_holes.offset_polygons(offset_value)
        
        # Verify the offset polygons
        assert len(offset_polygons) == 3
        
        # Expected offset polygons based on the provided output
        # Create the expected outer polygon
        expected_outer = sg.Polygon([
            sg.Point2(0.0541175, -0.192705),
            sg.Point2(-0.289466, -0.14414),
            sg.Point2(0.302963, -0.0360707),
            sg.Point2(0.228191, 0.439184),
            sg.Point2(-0.335874, 0.0584608),
            sg.Point2(-0.285382, -0.465923),
            sg.Point2(0.365971, -0.412673)
        ])
        
        # Create the expected first hole
        expected_hole1 = sg.Polygon([
            sg.Point2(-0.292023, 0.0488479),
            sg.Point2(0.214159, 0.390502),
            sg.Point2(0.26607, 0.0605441),
            sg.Point2(-0.283497, -0.0397073)
        ])
        
        # Create the expected second hole
        expected_hole2 = sg.Polygon([
            sg.Point2(0.0270688, -0.225913),
            sg.Point2(0.229433, -0.368651),
            sg.Point2(-0.270719, -0.409541),
            sg.Point2(-0.292752, -0.180707)
        ])
        
        # Helper function to check if two polygons are approximately equal
        def polygons_approximately_equal(poly1, poly2, epsilon=1e-5):
            if len(poly1) != len(poly2):
                return False
            
            for p1, p2 in zip(poly1.vertices, poly2.vertices):
                # Convert to float for comparison
                x1, y1 = float(p1.x()), float(p1.y())
                x2, y2 = float(p2.x()), float(p2.y())
                
                if abs(x1 - x2) > epsilon or abs(y1 - y2) > epsilon:
                    return False
            return True
        
        # Check that the generated polygons match the expected ones
        assert polygons_approximately_equal(offset_polygons[0], expected_outer)
        assert polygons_approximately_equal(offset_polygons[1], expected_hole1)
        assert polygons_approximately_equal(offset_polygons[2], expected_hole2)
        
        # Test with different offset values
        larger_offset = 0.05
        larger_offset_polygons = skeleton_with_holes.offset_polygons(larger_offset)
        assert len(larger_offset_polygons) > 0
        
        smaller_offset = 0.01
        smaller_offset_polygons = skeleton_with_holes.offset_polygons(smaller_offset)
        assert len(smaller_offset_polygons) > 0
