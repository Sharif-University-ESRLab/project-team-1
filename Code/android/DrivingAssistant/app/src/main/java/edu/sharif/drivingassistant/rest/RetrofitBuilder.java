package edu.sharif.drivingassistant.rest;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetrofitBuilder {
    private static final String API = "http://192.168.1.10:7000/";

    static Gson gson = new GsonBuilder().setLenient().create();

    private static final Retrofit RETROFIT = new Retrofit.Builder()
            .baseUrl(API)
            .addConverterFactory(GsonConverterFactory.create(gson)).build();

    public static TrajectoryApiInterface getApi() {
        return RETROFIT.create(TrajectoryApiInterface.class);
    }
}
