package edu.sharif.drivingassistant.ui;

import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.ToggleButton;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.Description;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.formatter.ValueFormatter;
import com.github.mikephil.charting.interfaces.datasets.ILineDataSet;

import edu.sharif.drivingassistant.R;
import edu.sharif.drivingassistant.db.dao.TrajectoryRepository;
import edu.sharif.drivingassistant.db.entity.TrajectoryRecord;
import edu.sharif.drivingassistant.services.ModelConverter;
import edu.sharif.drivingassistant.services.ThreadPoolService;
import edu.sharif.drivingassistant.util.DateConversionUtil;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.CompletableFuture;


public class ChartActivity extends AppCompatActivity {

    private static String LOG_TAG = "cca-TAG";

    private ModelConverter modelConverter;
    private ThreadPoolService threadPoolService;
    private LineChart lineChart;
    private ToggleButton dataToggle;
    private TrajectoryRepository trajectoryRepository;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.chart_main);
        lineChart = findViewById(R.id.line_chart);
        dataToggle = findViewById(R.id.data_toggle);
        dataToggle.setOnClickListener(view -> {
            configureLineChart();
            setLineChartData();
        });
        modelConverter = ModelConverter.getInstance();
        trajectoryRepository = TrajectoryRepository.getInstance(getBaseContext());
        threadPoolService = ThreadPoolService.getInstance();
        configureLineChart();
        setLineChartData();
    }

    private void configureLineChart() {
        Description desc = new Description();
        lineChart.setDescription(desc);

        XAxis xAxis = lineChart.getXAxis();
        xAxis.setDrawGridLines(true);
        xAxis.setGranularityEnabled(true);
        xAxis.setAxisMinimum(DateConversionUtil.getThreeDaysAgo() - DateConversionUtil.DAY_IN_MS);
        xAxis.setAxisMaximum(DateConversionUtil.getTodayEpoch());
        xAxis.setValueFormatter(new ValueFormatter() {
            private final SimpleDateFormat mFormat = new SimpleDateFormat("dd MMM", Locale.ENGLISH);

            @Override
            public String getFormattedValue(float value) {
                long millis = (long) value;
                return mFormat.format(new Date(millis));
            }
        });
        YAxis leftAxis = lineChart.getAxisLeft();
        leftAxis.setPosition(YAxis.YAxisLabelPosition.INSIDE_CHART);
        leftAxis.setDrawGridLines(true);
        leftAxis.setGranularityEnabled(true);
        leftAxis.setAxisMinimum(0f);
        leftAxis.setXOffset(-10f);
        if (!dataToggle.isChecked()){
            leftAxis.setAxisMaximum(20f);
        } else{
            leftAxis.setAxisMaximum(150f);
        }
        leftAxis.setEnabled(true);

        lineChart.getAxisRight().setEnabled(false);
    }

    private void setLineChartData() {
        CompletableFuture<Boolean> completableFutureLock = new CompletableFuture<>();
        ArrayList<Entry> averageSpeed = new ArrayList<>();
        ArrayList<Entry> distance = new ArrayList<>();
        threadPoolService.execute(() -> {
            try {
                List<TrajectoryRecord> records = trajectoryRepository.
                        getPastSevenDaysInfo(DateConversionUtil.getThreeDaysAgo());
                records.forEach(record -> {
                    averageSpeed.add(new Entry(record.getRecordDateEpochs(), record.getAverageSpeed()));
                    distance.add(new Entry(record.getRecordDateEpochs(), record.getDistance() / 1000));
                });
                completableFutureLock.complete(true);
            } catch (Exception e) {
                completableFutureLock.complete(false);
            }
        });
        completableFutureLock.join();
        ArrayList<ILineDataSet> dataSets = new ArrayList<>();

        if (dataToggle.isChecked()) {
            LineDataSet highLineDataSet = new LineDataSet(averageSpeed,
                    getResources().getString(R.string.average_speed));
            highLineDataSet.setAxisDependency(YAxis.AxisDependency.LEFT);
            highLineDataSet.setDrawCircles(true);
            highLineDataSet.setCircleRadius(4);
            highLineDataSet.setDrawValues(false);
            highLineDataSet.setLineWidth(2);
            highLineDataSet.setColor(Color.GREEN);
            highLineDataSet.setCircleColor(Color.GREEN);
            dataSets.clear();
            dataSets.add(highLineDataSet);
        }

        if (!dataToggle.isChecked()) {
            LineDataSet lowLineDataSet = new LineDataSet(distance,
                    getResources().getString(R.string.distance));
            lowLineDataSet.setDrawCircles(true);
            lowLineDataSet.setCircleRadius(4);
            lowLineDataSet.setDrawValues(false);
            lowLineDataSet.setLineWidth(3);
            lowLineDataSet.setColor(Color.RED);
            lowLineDataSet.setCircleColor(Color.RED);
            dataSets.clear();
            dataSets.add(lowLineDataSet);
        }

        LineData lineData = new LineData(dataSets);
        lineChart.setData(lineData);
        lineChart.invalidate();
    }
}
