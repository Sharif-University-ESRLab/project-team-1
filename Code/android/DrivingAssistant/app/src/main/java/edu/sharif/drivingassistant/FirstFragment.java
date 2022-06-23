package edu.sharif.drivingassistant;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import java.util.Objects;
import java.util.concurrent.atomic.AtomicInteger;

import edu.sharif.drivingassistant.databinding.FragmentFirstBinding;

public class FirstFragment extends Fragment {

    private FragmentFirstBinding binding;
    private NotificationCompat.Builder notifBuilder;
    private NotificationManagerCompat notifManager;
    private Integer notifId;
    private String channelId;
    private Context context;

    @Override
    public View onCreateView(
            LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {
        this.context = Objects.requireNonNull(getContext());
        Log.d("DALOG", "Check first");
        Log.d("DALOG", String.valueOf(getId()));
        Log.d("DALOG", String.valueOf(getArguments() == null));
        Bundle args = Objects.requireNonNull(getArguments());
        this.notifId = args.getInt("notifId");
        this.channelId = args.getString("channelId");
        this.notifBuilder = createNotificationBuilder();
        this.notifManager = NotificationManagerCompat.from(context);
        setArguments(args);
        binding = FragmentFirstBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);


        binding.buttonFirst.setOnClickListener(view1 -> {
            NavHostFragment.findNavController(FirstFragment.this)
                    .navigate(R.id.action_FirstFragment_to_SecondFragment);
            notifBuilder.setContentTitle("First title");
            notifBuilder.setContentText("First text");
            notifManager.notify(notifId, notifBuilder.build());
        });
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

    private NotificationCompat.Builder createNotificationBuilder() {
        return new NotificationCompat.
                Builder(this.context, this.channelId)
                .setSmallIcon(R.drawable.notification_icon)
                .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
                .setPriority(NotificationCompat.PRIORITY_DEFAULT);
    }

}