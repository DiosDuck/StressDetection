package com.example.frontend.okhttp;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class MultipleStressResponse {
    @SerializedName("results")
    @Expose
    private List<StressResponse> results;

    public List<StressResponse> getResults() {
        return results;
    }

    public void setResults(List<StressResponse> rezults) {
        this.results = rezults;
    }
}
