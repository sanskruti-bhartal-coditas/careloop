package org.project.javabackend.enums;

import lombok.Getter;

@Getter
public enum NotificationType {

    SCHEDULE("schedule"),
    NEW_REQUEST("new_request"),
    OTP("otp"),
    WELCOME("welcome"),
    PANEL_COMPLETE("panel_complete");

    private final String value;

    NotificationType(String value) {
        this.value = value;
    }
}