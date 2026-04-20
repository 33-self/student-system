package com.school.school_management.dto;
import lombok.Data;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

@Data
public class StudentRequest {
    @NotBlank
    private String name;
    private Integer gender;
    private Integer age;
    private String className;
}