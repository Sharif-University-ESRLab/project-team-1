package edu.sharif.drivingassistant.clients;


import android.content.res.Resources;
import android.util.Log;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.databind.ObjectMapper;
import edu.sharif.drivingassistant.R;
import edu.sharif.drivingassistant.model.exception.ApiConnectivityException;
import edu.sharif.drivingassistant.model.trajectory.GpsDTO;
import edu.sharif.drivingassistant.model.trajectory.TrajectoryDTO;
import edu.sharif.drivingassistant.services.ModelConverter;

import org.jetbrains.annotations.NotNull;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.util.Objects;
import java.util.concurrent.CompletableFuture;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class ApiService {
    private static final ApiService API_UTIL = new ApiService();
    private OkHttpClient client;
    private Resources resources;
    private ObjectMapper objectMapper;
    private ModelConverter converter;

    public static ApiService getInstance(Resources resources) {
        API_UTIL.resources = resources;
        API_UTIL.client = new OkHttpClient();
        API_UTIL.objectMapper = new ObjectMapper();
        API_UTIL.objectMapper.setVisibility(API_UTIL.objectMapper.getSerializationConfig().
                getDefaultVisibilityChecker()
                .withFieldVisibility(JsonAutoDetect.Visibility.ANY)
                .withGetterVisibility(JsonAutoDetect.Visibility.NONE)
                .withSetterVisibility(JsonAutoDetect.Visibility.NONE)
                .withCreatorVisibility(JsonAutoDetect.Visibility.NONE));
        API_UTIL.converter = ModelConverter.getInstance();
        return API_UTIL;
    }

    public TrajectoryDTO getTrajectoryInfo() throws ApiConnectivityException {
        Request request = buildFetchCoinsInfoRequest();
        CompletableFuture<TrajectoryDTO> lockCompletableFuture = new CompletableFuture<>();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                Log.wtf("Api", "getCoinsInfo->onFailure: ", e);
                lockCompletableFuture.complete(null);
            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                if (response.code() == HttpURLConnection.HTTP_OK) {
                    String responseBody = Objects.requireNonNull(response.body()).string();
                    GpsDTO gpsDTO = objectMapper.reader().readValue(responseBody, GpsDTO.class);
                    TrajectoryDTO trajectoryDTO = converter.getTrajectoryDTO(gpsDTO);
                    lockCompletableFuture.complete(trajectoryDTO);
                } else {
                    Log.e("Api", "getCoinsInfo->onResponse code: " + response.code());
                    lockCompletableFuture.complete(null);
                }
            }
        });
        TrajectoryDTO result = lockCompletableFuture.join();
        if (result == null)
            throw new ApiConnectivityException();
        return result;
    }

    private Request buildFetchCoinsInfoRequest() {
        HttpUrl.Builder urlBuilder = Objects.requireNonNull(HttpUrl.parse(resources.getString(R.string.info_api))).
                newBuilder();
        return new Request.Builder().url(urlBuilder.build().toString()).build();
    }
}
