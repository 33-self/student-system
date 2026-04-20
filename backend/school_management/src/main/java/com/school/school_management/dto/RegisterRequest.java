package com.school.school_management.dto;

import lombok.Data;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

@Data
public class RegisterRequest {
    @NotBlank(message = "工号不能为空")
    @Pattern(regexp = "^[0-9]{6,12}$", message = "工号格式错误：仅限6-12位数字")
    private String username;
    
    @NotBlank(message = "密码不能为空")
    private String password;
}