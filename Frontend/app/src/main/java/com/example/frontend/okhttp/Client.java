package com.example.frontend.okhttp;

import java.util.List;

import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface Client {
    @GET("/start/")
    Call<Repo> homeGet();

    @Multipart
    @POST("/save/")
    Call<ResponseBody> upload(
                    @Part("name") RequestBody name,
                    @Part MultipartBody.Part audio
            );

    @Multipart
    @POST("/predict/")
    Call<PredictBody> predict(
            @Part("name") RequestBody name,
            @Part MultipartBody.Part audio
    );
}
