package edu.sharif.drivingassistant.db.dao;

import static android.provider.BaseColumns._ID;
import static edu.sharif.drivingassistant.db.entity.TrajectoryRecordEntry.*;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;

import java.util.ArrayList;
import java.util.List;

import edu.sharif.drivingassistant.db.entity.TrajectoryRecord;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class TrajectoryRepository {
    private static final TrajectoryRepository TRAJECTORY_REPOSITORY = new TrajectoryRepository();
    private TrajectoryDBHelper trajectoryDBHelper;

    public static TrajectoryRepository getInstance(Context context) {
        TRAJECTORY_REPOSITORY.trajectoryDBHelper = new TrajectoryDBHelper(context);
        return TRAJECTORY_REPOSITORY;
    }

    public List<TrajectoryRecord> getPastSevenDaysInfo(long epochs) {
        SQLiteDatabase db = trajectoryDBHelper.getReadableDatabase();
        String[] columns = {_ID, RECORD_DATE, DISTANCE, AVERAGE_SPEED,
                DRIVING_TIME_SECONDS};
        Cursor cursor = db.query(TABLE_NAME, columns, RECORD_DATE + " >= ?",
                new String[]{String.valueOf(epochs)}, null, null, null, null);
        List<TrajectoryRecord> records = new ArrayList<>();
        while (cursor.moveToNext()) {
            records.add(readTrajectory(cursor));
        }
        cursor.close();
        return records;
    }

    private TrajectoryRecord readTrajectory(Cursor cursor) {
        TrajectoryRecord trajectoryRecord = new TrajectoryRecord();
        trajectoryRecord.setDbId(cursor.getLong(cursor.getColumnIndexOrThrow(_ID)));
        trajectoryRecord.setDistance(cursor.getFloat(cursor.getColumnIndexOrThrow(DISTANCE)));
        trajectoryRecord.setRecordDateEpochs(cursor.getLong(cursor.getColumnIndexOrThrow(RECORD_DATE)));
        trajectoryRecord.setDrivingTimeSeconds(cursor.getInt(cursor.getColumnIndexOrThrow(DRIVING_TIME_SECONDS)));
        trajectoryRecord.setAverageSpeed(cursor.getFloat(cursor.getColumnIndexOrThrow(AVERAGE_SPEED)));
        return trajectoryRecord;
    }

    public void putTrajectory(TrajectoryRecord record) {
        SQLiteDatabase db = trajectoryDBHelper.getWritableDatabase();
        db.insert(TABLE_NAME, null, setTrajectoryValues(record));
    }

    public void updateTrajectories(TrajectoryRecord record) {
        SQLiteDatabase db = trajectoryDBHelper.getWritableDatabase();
        String selection = RECORD_DATE + " = ?";
        String[] args = new String[]{String.valueOf(record.getRecordDateEpochs())};
        Cursor sameDayRecordCursor = db.query(TABLE_NAME, null, selection, args,
                null, null, null);
        if (sameDayRecordCursor.moveToLast()){
            float distance = sameDayRecordCursor.getFloat(sameDayRecordCursor.
                    getColumnIndexOrThrow(DISTANCE));
            int drivingTimeSeconds = sameDayRecordCursor.getInt(sameDayRecordCursor.
                    getColumnIndexOrThrow(DRIVING_TIME_SECONDS));
            record.setDistance(record.getDistance() + distance);
            record.setDrivingTimeSeconds(1 + drivingTimeSeconds);
            record.setAverageSpeed((float) (record.getDistance() * 3.6 /
                    (record.getDrivingTimeSeconds())));
            db.update(TABLE_NAME, setTrajectoryValues(record), selection, args);
        } else {
            record.setDrivingTimeSeconds(1);
            putTrajectory(record);
        }
    }

    public void deleteTrajectories() {
        SQLiteDatabase db = trajectoryDBHelper.getWritableDatabase();
        db.delete(TABLE_NAME, null, null);
    }

    private ContentValues setTrajectoryValues(TrajectoryRecord trajectoryRecord) {
        ContentValues values = new ContentValues();
        values.put(RECORD_DATE, trajectoryRecord.getRecordDateEpochs());
        values.put(DISTANCE, trajectoryRecord.getDistance());
        values.put(DRIVING_TIME_SECONDS, trajectoryRecord.getDrivingTimeSeconds());
        values.put(AVERAGE_SPEED, trajectoryRecord.getAverageSpeed());
        return values;
    }
}
