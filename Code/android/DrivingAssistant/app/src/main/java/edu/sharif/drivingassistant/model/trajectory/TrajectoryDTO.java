package edu.sharif.drivingassistant.model.trajectory;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@NoArgsConstructor
@Data
public class TrajectoryDTO {
    @NonNull
    private String distance;
    @NonNull
    private String averageSpeed;
    @NonNull
    private String limit;

    private static final TrajectoryDTO FAILED = new TrajectoryDTO("-", "-",
            "-");

    public static TrajectoryDTO getFailed() {
        return FAILED;
    }
}
