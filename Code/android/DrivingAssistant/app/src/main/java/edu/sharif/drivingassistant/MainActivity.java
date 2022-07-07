package edu.sharif.drivingassistant;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.TaskStackBuilder;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

import edu.sharif.drivingassistant.clients.ApiService;
import edu.sharif.drivingassistant.db.dao.TrajectoryRepository;
import edu.sharif.drivingassistant.db.entity.TrajectoryRecord;
import edu.sharif.drivingassistant.model.exception.ApiConnectivityException;
import edu.sharif.drivingassistant.model.trajectory.TrajectoryDTO;
import edu.sharif.drivingassistant.services.ModelConverter;
import edu.sharif.drivingassistant.services.ThreadPoolService;
import edu.sharif.drivingassistant.ui.ChartActivity;

import android.widget.Button;
import android.widget.TextView;

import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.CompletableFuture;

public class MainActivity extends AppCompatActivity {

    private static final String CHANNEL_ID = "DA_CHANNEL";
    private static final Integer NOTIF_ID = 1;
    private ApiService apiService;
    private TrajectoryRepository trajectoryRepository;
    private ModelConverter modelConverter;
    private ThreadPoolService threadPoolService;
    private Timer timer = new Timer();
    private TimerTask timerTask;
    private NotificationManagerCompat notificationManagerCompat;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Bundle args = new Bundle();
        args.putInt("notifId", 0);
        args.putString("channelId", CHANNEL_ID);
        apiService = ApiService.getInstance(getResources());
        trajectoryRepository = TrajectoryRepository.getInstance(getBaseContext());
        modelConverter = ModelConverter.getInstance();
        threadPoolService = ThreadPoolService.getInstance();
        createNotificationChannel();
        Button historyButton = findViewById(R.id.chart_button);
        historyButton.setOnClickListener(view -> {
            Intent intent = new Intent(MainActivity.this, ChartActivity.class);
            startActivity(intent);
        });
        refreshSpeedSchedule();
    }

    private TrajectoryDTO fetch_trajectory() {
        try {
            TrajectoryDTO trajectoryDTO = apiService.getTrajectoryInfo();
            TrajectoryRecord record = modelConverter.getTrajectoryEntity(trajectoryDTO);
            trajectoryRepository.updateTrajectories(record);
            return trajectoryDTO;
        } catch (ApiConnectivityException e) {
            return TrajectoryDTO.getFailed();
        }
    }

    private void createNotificationChannel() {
        String channelName = "DA channel";
        String channelDescription = "A notification channel for Driving Assistant app";
        int importance = NotificationManager.IMPORTANCE_DEFAULT;
        NotificationChannel channel = new NotificationChannel(CHANNEL_ID, channelName, importance);
        channel.setDescription(channelDescription);
        NotificationManager notificationManager = getSystemService(NotificationManager.class);
        notificationManager.createNotificationChannel(channel);
        notificationManagerCompat = NotificationManagerCompat.from(this);
    }

    private void refreshSpeedSchedule() {
        timerTask = new TimerTask() {
            @Override
            public void run() {
                CompletableFuture<TrajectoryDTO> speedFuture = new CompletableFuture();
                threadPoolService.execute(() -> {
                    TrajectoryDTO trajectory = fetch_trajectory();
                    speedFuture.complete(trajectory);
                });
                TrajectoryDTO trajectory = speedFuture.join();
                runOnUiThread(() -> {
                    TextView speed = findViewById(R.id.speed);
                    TextView speedInfo = findViewById(R.id.speed_info);
                    TextView speedLimit = findViewById(R.id.limit);
                    String averageSpeed = trajectory.getAverageSpeed();
                    String limit = trajectory.getLimit();
                    speed.setText(averageSpeed);
                    speedLimit.setText(limit);
                    if (trajectory.equals(TrajectoryDTO.getFailed())) {
                        speedInfo.setTextColor(Color.GRAY);
                    } else {
                        alertDriver(Float.parseFloat(averageSpeed), Integer.parseInt(limit),
                                speedInfo);
                    }
                });
            }
        };
        timer.schedule(timerTask, 1000, 1000);
    }

    private void alertDriver(float speed, int limit, TextView speedInfo) {
        String notifText;
        if (speed > limit) {
            speedInfo.setTextColor(Color.RED);
            notifText = "Exceeding speed: " + speed + " while the limit is " + limit;
        } else {
            speedInfo.setTextColor(Color.GRAY);
            notifText = "Speed: " + speed + " limit: " + limit;
        }
        Intent intent = new Intent(this, MainActivity.class);
        TaskStackBuilder stackBuilder = TaskStackBuilder.create(this);
        stackBuilder.addNextIntentWithParentStack(intent);
        PendingIntent resultPendingIntent = stackBuilder.getPendingIntent(0,
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setSmallIcon(R.drawable.notification_icon)
                .setContentTitle("Speed notification")
                .setContentText(notifText)
                .setContentIntent(resultPendingIntent)
                .setAutoCancel(false);
        notificationManagerCompat.notify(NOTIF_ID, builder.build());
    }
}