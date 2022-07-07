package edu.sharif.drivingassistant.db.dao;

import static edu.sharif.drivingassistant.db.entity.TrajectoryRecordEntry.SQL_CREATE_ENTRIES;
import static edu.sharif.drivingassistant.db.entity.TrajectoryRecordEntry.SQL_DELETE_ENTRIES;

import static edu.sharif.drivingassistant.db.entity.TrajectoryRecordEntry.SQL_CREATE_ENTRIES;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import androidx.annotation.Nullable;

public class TrajectoryDBHelper extends SQLiteOpenHelper {
    static final String DATABASE_NAME = "driver_db";
    static final Integer DATABASE_VERSION = 1;

    public TrajectoryDBHelper(@Nullable Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onDowngrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        onUpgrade(db, oldVersion, newVersion);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(SQL_CREATE_ENTRIES);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL(SQL_DELETE_ENTRIES);
    }
}
