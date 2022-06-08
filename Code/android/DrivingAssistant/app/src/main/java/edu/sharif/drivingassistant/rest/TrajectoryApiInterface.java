package edu.sharif.drivingassistant.rest;

import edu.sharif.drivingassistant.model.TrajectoryInfo;
import retrofit2.Call;
import retrofit2.http.GET;

public interface TrajectoryApiInterface {
    @GET("trajectory_info")
    Call<TrajectoryInfo> getTrajectory();
}
