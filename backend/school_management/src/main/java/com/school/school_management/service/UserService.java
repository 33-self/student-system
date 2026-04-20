package com.school.school_management.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.school.school_management.dto.LoginResponse;
import com.school.school_management.dto.RegisterRequest;
import com.school.school_management.entity.User;

public interface UserService extends IService<User> {
    void register(RegisterRequest request);
    LoginResponse login(String username, String password);
}