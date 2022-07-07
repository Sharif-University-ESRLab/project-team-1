package edu.sharif.drivingassistant.services;

import android.annotation.SuppressLint;
import android.util.Log;

import edu.sharif.drivingassistant.db.entity.TrajectoryRecord;

import edu.sharif.drivingassistant.model.trajectory.GpsDTO;
import edu.sharif.drivingassistant.model.trajectory.TrajectoryDTO;
import edu.sharif.drivingassistant.util.DateConversionUtil;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class ModelConverter {
    private static final ModelConverter MODEL_CONVERTER = new ModelConverter();

    public static ModelConverter getInstance() {
        return MODEL_CONVERTER;
    }

    public TrajectoryRecord getTrajectoryEntity(TrajectoryDTO trajectoryDTO) {
        TrajectoryRecord trajectoryRecord = new TrajectoryRecord();
        trajectoryRecord.setAverageSpeed(Float.parseFloat(trajectoryDTO.getAverageSpeed()));
        trajectoryRecord.setDistance(Float.parseFloat(trajectoryDTO.getDistance()));
        trajectoryRecord.setRecordDateEpochs(DateConversionUtil.getTodayEpoch());
        return trajectoryRecord;
    }

    @SuppressLint("DefaultLocale")
    public TrajectoryDTO getTrajectoryDTO(GpsDTO gpsDTO) {
        return new TrajectoryDTO(String.valueOf(gpsDTO.getDistance()),
                String.format("%.2f", gpsDTO.getDistance() * 3.6), String.valueOf(gpsDTO.getLimit()));
    }
}
