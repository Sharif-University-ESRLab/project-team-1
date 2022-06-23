package edu.sharif.drivingassistant;

import android.content.Context;
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

import edu.sharif.drivingassistant.databinding.FragmentSecondBinding;

public class SecondFragment extends Fragment {

    private FragmentSecondBinding binding;
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
        Log.d("DALOG", "Check second");
        this.context = Objects.requireNonNull(getContext());
        Bundle args = Objects.requireNonNull(getArguments());
        this.notifId = args.getInt("notifId");
        this.channelId = args.getString("channelId");
        this.notifBuilder = createNotificationBuilder();
        this.notifManager = NotificationManagerCompat.from(context);
        setArguments(args);

        binding = FragmentSecondBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        binding.buttonSecond.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                NavHostFragment.findNavController(SecondFragment.this)
                        .navigate(R.id.action_SecondFragment_to_FirstFragment);
                notifBuilder.setContentTitle("Second title");
                notifBuilder.setContentText("Second text");
                notifManager.notify(notifId, notifBuilder.build());
            }
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