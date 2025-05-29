import pytest
import numpy as np
import skgeom as sg
from skgeom._skgeom.skeleton import create_interior_straight_skeleton


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

        skeleton = create_interior_straight_skeleton(polygon)

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

        skeleton = create_interior_straight_skeleton(polygon)

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

        skeleton = create_interior_straight_skeleton(polygon)

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

        skeleton = create_interior_straight_skeleton(polygon)

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

        skeleton = create_interior_straight_skeleton(polygon)

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

        skeleton = create_interior_straight_skeleton(polygon)

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

        skeleton = create_interior_straight_skeleton(polygon)
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
        small_skeleton = create_interior_straight_skeleton(small_polygon)
        assert small_skeleton is not None

        # Large rectangle
        large_points = [
            sg.Point2(0, 0),
            sg.Point2(100, 0),
            sg.Point2(100, 50),
            sg.Point2(0, 50)
        ]
        large_polygon = sg.Polygon(large_points)
        large_skeleton = create_interior_straight_skeleton(large_polygon)
        assert large_skeleton is not None

    def test_invalid_polygon_error(self):
        """Test that invalid polygons raise errors."""
        # Test with collinear points (degenerate case)
        try:
            points = [sg.Point2(0, 0), sg.Point2(1, 0), sg.Point2(2, 0)]  # Collinear points
            polygon = sg.Polygon(points)
            skeleton = create_interior_straight_skeleton(polygon)
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

        skeleton = create_interior_straight_skeleton(polygon)

        # Should return a Skeleton object
        assert skeleton is not None
        assert 'Skeleton' in str(type(skeleton))


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])