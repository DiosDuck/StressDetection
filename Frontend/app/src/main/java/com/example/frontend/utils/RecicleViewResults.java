package com.example.frontend.utils;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.frontend.R;
import com.example.frontend.okhttp.StressResponse;

import java.util.List;

public class RecicleViewResults extends RecyclerView.Adapter<RecicleViewResults.ResultsViewHolder> {
    private List<StressResponse> stressResponses;

    public RecicleViewResults(List<StressResponse> stressResponses) {
        this.stressResponses = stressResponses;
    }

    public class ResultsViewHolder extends RecyclerView.ViewHolder{

        private TextView sentenceText;
        private TextView resultText;

        public ResultsViewHolder(@NonNull View itemView) {
            super(itemView);
            sentenceText= itemView.findViewById(R.id.sentence);
            resultText=itemView.findViewById(R.id.result);
        }
    }

    @NonNull
    @Override
    public RecicleViewResults.ResultsViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView= LayoutInflater.from(parent.getContext()).inflate(R.layout.list_results,parent,false);
        return new ResultsViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull RecicleViewResults.ResultsViewHolder holder, int position) {
        String sentence=stressResponses.get(position).getSentence();
        String result=stressResponses.get(position).getResult();
        holder.sentenceText.setText(sentence);
        holder.resultText.setText(result);
    }

    @Override
    public int getItemCount() {
        return stressResponses.size();
    }
}
