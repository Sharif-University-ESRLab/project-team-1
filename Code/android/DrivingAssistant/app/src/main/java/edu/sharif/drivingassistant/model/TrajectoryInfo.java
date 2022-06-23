package edu.sharif.drivingassistant.model;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class TrajectoryInfo {
    private double speed;
    private double latitude;
    private double longitude;
}
