package org.project.javabackend.enums;

import lombok.Getter;

@Getter
public enum ReviewerName {

    SUMMARIZER("summarizer"),
    DOCUMENT_CHECKER("document_checker"),
    PRIORITY_REVIEWER("priority_reviewer"),
    CONSISTENCY_REVIEWER("consistency_reviewer");

    private final String value;

    ReviewerName(String value) {
        this.value = value;
    }
}