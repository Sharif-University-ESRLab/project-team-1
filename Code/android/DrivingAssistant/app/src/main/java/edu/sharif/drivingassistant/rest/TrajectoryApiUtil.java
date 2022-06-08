package edu.sharif.drivingassistant.rest;

import java.util.concurrent.CompletableFuture;

import edu.sharif.drivingassistant.model.TrajectoryInfo;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class TrajectoryApiUtil {
    public void getTrajectoryInfo(CompletableFuture<TrajectoryInfo> future){
        TrajectoryApiInterface apiInterface = RetrofitBuilder.getApi();
        Call<TrajectoryInfo> getTrajectoryCall = apiInterface.getTrajectory();
        getTrajectoryCall.enqueue(new Callback<TrajectoryInfo>() {
            @Override
            public void onResponse(Call<TrajectoryInfo> call, Response<TrajectoryInfo> response) {
                if (response.isSuccessful()){
                    TrajectoryInfo info = response.body();
                    future.complete(info);
                } else {
                    future.complete(null);
                }
            }

            @Override
            public void onFailure(Call<TrajectoryInfo> call, Throwable t) {
                future.complete(null);
            }
        });
    }
}
