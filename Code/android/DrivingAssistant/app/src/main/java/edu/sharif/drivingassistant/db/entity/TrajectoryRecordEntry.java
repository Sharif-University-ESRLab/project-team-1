package edu.sharif.drivingassistant.db.entity;

import android.provider.BaseColumns;

public class TrajectoryRecordEntry implements BaseColumns {
    public static final String TABLE_NAME = "trajectory_table";
    public static final String RECORD_DATE = "record_date_epochs";
    public static final String DISTANCE = "distance";
    public static final String AVERAGE_SPEED = "average_speed";
    public static final String DRIVING_TIME_SECONDS = "driving_time_seconds";
    public static final String SQL_CREATE_ENTRIES = "CREATE TABLE " + TABLE_NAME +
            "(" +
            _ID + " INTEGER PRIMARY KEY," +
            RECORD_DATE + " INTEGER," +
            DISTANCE + " DOUBLE," +
            AVERAGE_SPEED + " DOUBLE," +
            DRIVING_TIME_SECONDS + " INTEGER" +
            ")";
    public static final String SQL_DELETE_ENTRIES = "DROP TABLE IF EXISTS " + TABLE_NAME;
}
