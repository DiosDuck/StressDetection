package com.example.frontend.okhttp;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class PredictBody {
    @SerializedName("message")
    @Expose
    private String message;

    @SerializedName("stress")
    @Expose
    private String stress;

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getStress() {
        return stress;
    }

    public void setStress(String stress) {
        this.stress = stress;
    }
}
