package com.example.frontend.okhttp;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class StressResponse {
    @SerializedName("message")
    @Expose
    private String sentence;

    @SerializedName("stress")
    @Expose
    private String result;

    public String getSentence() {
        return sentence;
    }

    public void setSentence(String message) {
        this.sentence = message;
    }

    public String getResult() {
        return result;
    }

    public void setResult(String stress) {
        this.result = stress;
    }
}
