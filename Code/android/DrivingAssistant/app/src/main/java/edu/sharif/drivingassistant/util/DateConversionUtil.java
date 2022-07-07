package edu.sharif.drivingassistant.util;

import java.sql.Timestamp;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneId;
import java.util.Date;

public class DateConversionUtil {
    public static final Long DAY_IN_MS = 1000L * 60 * 60 * 24;

    public static Long getEpoch(String date) {
        return -1L;
    }

    public static String getDateStr(Long epochs) {
        LocalDate localDate = Instant.ofEpochMilli(epochs).atZone(ZoneId.systemDefault()).toLocalDate();
        return localDate.toString();
    }

    public static Long getTodayEpoch() {
        long currentEpoch = System.currentTimeMillis();
        return (currentEpoch - currentEpoch % DAY_IN_MS);
    }

    public static Long getThreeDaysAgo() {
        LocalDateTime now = LocalDateTime.now();
        return now.with(LocalTime.MIN).atZone(ZoneId.systemDefault()).toInstant().
                toEpochMilli() - (3 * DAY_IN_MS);
    }
}
