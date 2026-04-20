package com.school.school_management.controller;

import com.school.school_management.dto.LoginRequest;
import com.school.school_management.dto.LoginResponse;
import com.school.school_management.dto.RegisterRequest;
import com.school.school_management.service.UserService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public java.util.Map<String, String> register(@Valid @RequestBody RegisterRequest request) {
        userService.register(request);
        java.util.Map<String, String> result = new java.util.HashMap<>();
        result.put("message", "注册成功");
        return result;
    }

    @PostMapping("/login")
    public LoginResponse login(@Valid @RequestBody LoginRequest request) {
        return userService.login(request.getUsername(), request.getPassword());
    }
}