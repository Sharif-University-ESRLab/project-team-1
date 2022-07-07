package edu.sharif.drivingassistant.db.entity;

import java.sql.Date;
import java.sql.Time;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Data
public class TrajectoryRecord {
    private Long dbId;
    private Long recordDateEpochs;
    private Float distance;
    private Float averageSpeed;
    private Integer drivingTimeSeconds;
}
