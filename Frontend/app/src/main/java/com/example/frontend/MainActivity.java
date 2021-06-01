package com.example.frontend;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.Manifest;
import android.content.pm.PackageManager;
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.TextView;
import android.widget.Toast;

import com.example.frontend.okhttp.Client;
import com.example.frontend.okhttp.MultipleStressResponse;
import com.example.frontend.okhttp.StressResponse;
import com.example.frontend.utils.PCMtoWAV;
import com.example.frontend.utils.RecicleViewResults;;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity {

    private String baseURL="http://192.168.1.206:8000";
    OkHttpClient.Builder httpClient = new OkHttpClient.Builder();
    private TextView text;

    private Button send,stop,record;

    private List<StressResponse> stressResponseList;
    private RecyclerView recicleViewResults;

    private MediaRecorder mediaRecorder;
    private String outputFile,outputFilePCM;

    private AudioRecord audioRecord=null;
    private Thread recordingThread = null;
    private boolean isRecording = false;

    private int BufferElements2Rec = 1024; // want to play 2048 (2K) since 2 bytes we use only 1024
    private int BytesPerElement = 2; // 2 bytes in 16bit format


    private String language="RO";
    private String output="2";

    final int REQUEST_PERMISSION_CODE=1000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        stressResponseList=new ArrayList<>();
        text=(TextView) findViewById(R.id.text) ;

        send =findViewById(R.id.send);
        stop=findViewById(R.id.stop);
        record=findViewById(R.id.record);

        RecicleViewResults adaper=new RecicleViewResults(stressResponseList);
        recicleViewResults=findViewById(R.id.list_results);
        RecyclerView.LayoutManager layoutManager=new LinearLayoutManager(getApplicationContext());
        recicleViewResults.setLayoutManager(layoutManager);
        recicleViewResults.setItemAnimator(new DefaultItemAnimator());
        recicleViewResults.setAdapter(adaper);

        stop.setEnabled(false);
        send.setEnabled(false);
        outputFile = getFilesDir().getAbsolutePath() + "/recording.wav";
        outputFilePCM=getFilesDir().getAbsolutePath() + "/recording.pcm";
        text.setText("Waiting for a recording...");
        if(!checkPermissionFromDevice()){
            requestPermission();
        }
        record.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                if(checkPermissionFromDevice()) {
                    audioRecord = new AudioRecord(MediaRecorder.AudioSource.MIC,
                            16000, AudioFormat.CHANNEL_IN_MONO,
                            AudioFormat.ENCODING_PCM_16BIT, BufferElements2Rec * BytesPerElement);

                    audioRecord.startRecording();
                    isRecording = true;
                    recordingThread = new Thread(new Runnable() {
                        public void run() {
                            writeAudioDataToFile();
                        }
                    }, "AudioRecorder Thread");
                    recordingThread.start();
                    record.setEnabled(false);
                    stop.setEnabled(true);
                    send.setEnabled(false);

                    Toast.makeText(getApplicationContext(), "Recording started", Toast.LENGTH_LONG).show();
                }
                else{
                    requestPermission();
                }
            }
        });
        stop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (null != audioRecord) {
                    isRecording = false;
                    audioRecord.stop();
                    audioRecord.release();
                    audioRecord = null;
                    recordingThread = null;
                }
                record.setEnabled(true);
                stop.setEnabled(false);
                send.setEnabled(true);
                Toast.makeText(getApplicationContext(),"Recording stopped",Toast.LENGTH_LONG).show();
            }
        });
        send.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    PCMtoWAV.PCMToWAV(new File(outputFilePCM),new File(outputFile),1,16000,16);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                Retrofit.Builder builder=new Retrofit.Builder()
                        .baseUrl(baseURL)
                        .addConverterFactory(GsonConverterFactory.create());

                Retrofit retrofit=builder
                        .client(httpClient.build())
                        .build();
                Client client=retrofit.create(Client.class);

                RequestBody nameBody=RequestBody.create(MultipartBody.FORM,"test");

                File file=new File(outputFile);

                RequestBody fileBody=RequestBody.create(
                        MediaType.parse("audio/x-wav"),
                        file);

                MultipartBody.Part body=
                        MultipartBody.Part.createFormData("audio",file.getName(),fileBody);

                RequestBody languageBody=RequestBody.create(MultipartBody.FORM,language);

                RequestBody outputBody=RequestBody.create(MultipartBody.FORM,output);

                text.setText("Sending...");

                Call<MultipleStressResponse> call=client.predict(nameBody,body,languageBody,outputBody);

                call.enqueue(new Callback<MultipleStressResponse>() {
                    @Override
                    public void onResponse(Call<MultipleStressResponse> call, Response<MultipleStressResponse> response) {
                        if(response.isSuccessful()){
                            response.body();
                            stressResponseList.clear();
                            stressResponseList.addAll(response.body().getResults());
                            adaper.notifyDataSetChanged();
                            text.setText("Sent!");
                        }
                        else{
                            Toast.makeText(getApplicationContext(),response.errorBody().toString(),Toast.LENGTH_SHORT).show();
                        }
                        //Toast.makeText(getApplicationContext(),"Success",Toast.LENGTH_LONG).show();
                    }

                    @Override
                    public void onFailure(Call<MultipleStressResponse> call, Throwable t) {
                        text.setText(t.toString());
                    }
                });
            }
        });
    }

    private void requestPermission(){
        ActivityCompat.requestPermissions(this,new String[]{
                Manifest.permission.WRITE_EXTERNAL_STORAGE,
                Manifest.permission.READ_EXTERNAL_STORAGE,
                Manifest.permission.RECORD_AUDIO
        },REQUEST_PERMISSION_CODE);
    }


    private boolean checkPermissionFromDevice() {
        int write_external_storage_result= ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE);
        int record_audio_result=ContextCompat.checkSelfPermission(this,Manifest.permission.RECORD_AUDIO);
        int read_external_storage_result= ContextCompat.checkSelfPermission(this,Manifest.permission.READ_EXTERNAL_STORAGE);
        return write_external_storage_result== PackageManager.PERMISSION_GRANTED &&
                record_audio_result==PackageManager.PERMISSION_GRANTED &&
                read_external_storage_result==PackageManager.PERMISSION_GRANTED;

    }

    private byte[] short2byte(short[] sData) {
        int shortArrsize = sData.length;
        byte[] bytes = new byte[shortArrsize * 2];
        for (int i = 0; i < shortArrsize; i++) {
            bytes[i * 2] = (byte) (sData[i] & 0x00FF);
            bytes[(i * 2) + 1] = (byte) (sData[i] >> 8);
            sData[i] = 0;
        }
        return bytes;

    }

    private void writeAudioDataToFile() {
        // Write the output audio in byte

        String filePath = outputFilePCM;
        short sData[] = new short[BufferElements2Rec];

        FileOutputStream os = null;
        try {
            os = new FileOutputStream(filePath);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        while (isRecording) {
            // gets the voice output from microphone to byte format

            audioRecord.read(sData, 0, BufferElements2Rec);
            System.out.println("Short writing to file" + sData.toString());
            try {
                // // writes the data to file from buffer
                // // stores the voice buffer
                byte bData[] = short2byte(sData);
                os.write(bData, 0, BufferElements2Rec * BytesPerElement);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        try {
            os.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void clickLanguageRadio(View view) {
        boolean checked=((RadioButton) view).isChecked();
        switch (view.getId()){
            case R.id.language_ro:
                if (checked)
                    language="RO";
                break;
            case R.id.language_en:
                if (checked)
                    language="EN";
                break;
        }
    }

    public void clickOutputRadio(View view) {
        boolean checked=((RadioButton) view).isChecked();
        switch (view.getId()){
            case R.id.output_2:
                if (checked)
                    output="2";
                break;
            case R.id.output_4:
                if (checked)
                    output="4";
                break;
        }
    }
}