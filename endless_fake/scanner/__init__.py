import cv2

from .theme import *
from .utils import cleanup_mask, draw_line_with_direction, find_edge_from_overlap


class Scanner:
    def __init__(self):
        self.platform_mask = None
        self.coins_mask = None
        self.player_mask = None
        self.left_border_mask = None
        self.right_border_mask = None
        self.bottom_border_mask = None
        self.entrance_mask = None
        self.exit_mask = None
        self.shadow_mask = None

        self.shadows = []

    def _filter_masks(self, frame):
        platform_mask = cv2.inRange(frame, theme.platform_min, theme.platform_max)
        self.coins_mask = cv2.inRange(frame, theme.coin_min, theme.coin_max)
        self.platform_mask = cv2.bitwise_or(platform_mask, self.coins_mask)

        self.left_border_mask = cv2.inRange(frame, theme.left_border_min, theme.left_border_max)
        self.right_border_mask = cv2.inRange(frame, theme.right_border_min, theme.right_border_max)
        self.bottom_border_mask = cv2.inRange(frame, theme.bottom_border_min, theme.bottom_border_max)
        self.right_border_mask = cv2.bitwise_and(self.right_border_mask, cv2.bitwise_not(self.bottom_border_mask))

        self.player_mask = cv2.inRange(frame, theme.player_body_min, theme.player_body_max)
        self.entrance_mask = cv2.inRange(frame, theme.entrance_min, theme.entrance_max)
        self.exit_mask = cv2.inRange(frame, theme.exit_min, theme.exit_max)

        self.platform_mask = cleanup_mask(self.platform_mask)
        self.left_border_mask = cleanup_mask(self.left_border_mask)
        self.right_border_mask = cleanup_mask(self.right_border_mask)
        self.bottom_border_mask = cleanup_mask(self.bottom_border_mask)
        self.player_mask = cleanup_mask(self.player_mask)
        self.entrance_mask = cleanup_mask(self.entrance_mask)
        self.exit_mask = cleanup_mask(self.exit_mask)

    def _filter_shadows(self, frame):
        pathshadow = cv2.inRange(frame, theme.player_shadow_min, theme.player_shadow_max)
        coinshadow = cv2.inRange(frame, theme.coin_shadow_min, theme.coin_shadow_max)
        shadow_mask = cv2.bitwise_or(pathshadow, coinshadow)
        self.shadow_mask = cleanup_mask(shadow_mask)

        self.shadows = []
        cnts, _ = cv2.findContours(self.shadow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        filtered = list(filter(lambda c: cv2.contourArea(c) > 80.0, cnts))
        for cnt in filtered:
            sample = np.zeros(self.shadow_mask.shape, dtype=np.uint8)
            cv2.drawContours(sample, [cnt], 0, 255, 2)

            merged = cv2.bitwise_and(sample, self.platform_mask)
            if cv2.countNonZero(merged) < 10:
                continue

            try:
                coords, center, angle = cv2.fitEllipse(cv2.convexHull(cnt, False))
                coords = (coords[0], coords[1])
                self.shadows.append((coords, center, angle))
            except Exception:
                continue

    def _confirm_player(self, coords):
        int_coords = (int(coords[0]), int(coords[1]))
        sample = np.zeros(self.player_mask.shape, dtype=np.uint8)
        cv2.line(sample, int_coords, (int_coords[0], int_coords[1] - 128), 255, 10)
        result = cv2.bitwise_and(sample, self.player_mask)
        count = cv2.countNonZero(result)
        return count

    def _get_player_angle(self, coords):
        left_border_sample = np.zeros(self.left_border_mask.shape, dtype=np.uint8)
        draw_line_with_direction(left_border_sample, coords, -56.5, 255, length=10)
        left_border_overlap = cv2.bitwise_and(left_border_sample, self.left_border_mask)

        right_border_sample = np.zeros(self.right_border_mask.shape, dtype=np.uint8)
        draw_line_with_direction(right_border_sample, coords, 56.5, 255, length=10)
        right_border_overlap = cv2.bitwise_and(right_border_sample, self.right_border_mask)

        left_border_size = 0
        if cv2.countNonZero(left_border_overlap) > 0:
            left_border_size = find_edge_from_overlap(self.left_border_mask, left_border_overlap)

        right_border_size = 0
        if cv2.countNonZero(right_border_overlap) > 0:
            right_border_size = find_edge_from_overlap(self.right_border_mask, right_border_overlap)

        if right_border_size == 0 and left_border_size == 0:
            return 0

        if right_border_size > left_border_size:
            return -56.5

        return 56.5

    def _get_player_distance(self, coords, direction):
        if direction == -56.5:
            opposite = self.left_border_mask
        elif direction == 56.5:
            opposite = self.right_border_mask
        else:
            opposite = self.bottom_border_mask

        sample = np.zeros(opposite.shape, dtype=np.uint8)
        draw_line_with_direction(sample, coords, direction, 255, length=100)

        result = cv2.bitwise_and(sample, opposite)

        if cv2.countNonZero(result) < 1:
            return None, None

        dots = []
        cnts, _ = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in cnts:
            m = cv2.moments(cnt)
            if m["m00"] == 0:
                continue
            cx = int(m["m10"] / m["m00"])
            cy = int(m["m01"] / m["m00"])
            endpoint = np.array([cx, cy])
            dots.append((np.linalg.norm(endpoint - coords), endpoint))

        if len(dots) < 1:
            return None, None

        return sorted(dots)[0]

    def _get_gap_length(self, edge_coords, direction):
        origin = np.array(edge_coords)
        sample = np.zeros(self.platform_mask.shape, dtype=np.uint8)
        draw_line_with_direction(sample, edge_coords, direction, 255, length=100, offset=5)
        result = cv2.bitwise_and(sample, self.platform_mask)

        if cv2.countNonZero(result) < 1:
            return None, None

        dots = []
        cnts, _ = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in cnts:
            points = np.squeeze(cnt)
            cx = None
            cy = None

            if len(points.shape) == 1:
                cx = points[0]
                cy = points[1]
            elif direction == 0:
                cx = np.sum(points, axis=0)[0] / len(cnt)
                cy = sorted(points, key=lambda x: x[1])[0][1]
            elif direction == -56.5:
                highest = sorted(points, reverse=False, key=lambda x: x[1])[0]
                rightest = sorted(points, reverse=True, key=lambda x: x[0])[0]
                cx = (highest[0] + rightest[0]) / 2
                cy = (highest[1] + rightest[1]) / 2
            elif direction == 56.5:
                highest = sorted(points, reverse=False, key=lambda x: x[1])[0]
                leftest = sorted(points, reverse=False, key=lambda x: x[0])[0]
                cx = (highest[0] + leftest[0]) / 2
                cy = (highest[1] + leftest[1]) / 2

            if cx is None and cy is None:
                continue

            target = (cx, cy)
            dots.append((np.linalg.norm(target - origin), target))
        if len(dots) < 1:
            return None, None

        return sorted(dots)[0]

    def _filter_players(self):
        self.players = []
        for shadow in self.shadows:
            coords, center, angle = shadow

            height = self._confirm_player(coords)
            if height < 75:
                continue

            direction = self._get_player_angle(coords)

            distance, edge_coords = self._get_player_distance(coords, direction)
            if distance is None:
                continue

            gap_length, end_coords = self._get_gap_length(edge_coords, direction)
            if gap_length is None:
                continue

            next_length, next_coords = self._get_player_distance(end_coords, direction)
            if next_length is None:
                next_length = 100

            line = {
                "direction": direction,
                "distance": distance,
                "edge_coords": edge_coords,
                "gap_length": gap_length,
                "end_coords": end_coords,
                "next_length": next_length
            }

            self.players.append((coords, center, angle, line))

    def _ingame(self, frame):
        coins = cv2.inRange(frame[5:20, 300:310], theme.coin_min, theme.coin_max)
        if np.sum(coins == 255) > 50:
            return True
        return False

    def process(self, frame):
        if not self._ingame(frame):
            return None

        self._filter_masks(frame)
        self._filter_shadows(frame)
        self._filter_players()

        lines = []
        for player in self.players:
            coords, center, angle, line = player
            lines.append(line)

        if len(lines) > 0:
            shortest = sorted(lines, key=lambda l: l["distance"])[0]
            return [
                round(shortest["distance"]),
                round(shortest["gap_length"]),
                round(shortest["next_length"])
            ]

        return None

    def debug_draw(self, frame):
        for player in self.players:
            coords, center, angle, line = player
            cv2.ellipse(frame, (coords, center, angle), (64, 64, 64), 2)

            draw_line_with_direction(frame, coords, line["direction"], (0, 0, 192), length=line["distance"],
                                     thickness=3)
            draw_line_with_direction(frame, line["edge_coords"], line["direction"], (192, 0, 0),
                                     length=line["gap_length"], thickness=3)
            draw_line_with_direction(frame, line["end_coords"], line["direction"], (0, 192, 0),
                                     length=line["next_length"], thickness=3)
