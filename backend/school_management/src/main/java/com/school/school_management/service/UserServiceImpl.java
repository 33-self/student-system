package com.school.school_management.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.school.school_management.dto.LoginResponse;
import com.school.school_management.dto.RegisterRequest;
import com.school.school_management.entity.User;
import com.school.school_management.mapper.UserMapper;
import com.school.school_management.service.UserService;
import com.school.school_management.utils.JwtUtil;
import com.school.school_management.utils.PasswordUtil;
import com.school.school_management.utils.PasswordValidator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    @Autowired
    private PasswordUtil passwordUtil;

    @Autowired
    private JwtUtil jwtUtil;

    @Override
    public void register(RegisterRequest request) {
        try {
            LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
            wrapper.eq(User::getUsername, request.getUsername());
            if (this.count(wrapper) > 0) {
                throw new RuntimeException("工号已存在，请使用其他工号");
            }
            
            if (!PasswordValidator.isValid(request.getPassword())) {
                throw new RuntimeException(PasswordValidator.getValidationMessage(request.getPassword()));
            }
            
            User user = new User();
            user.setUsername(request.getUsername());
            user.setPassword(passwordUtil.encode(request.getPassword()));
            user.setStatus(1);
            user.setRole(0);
            this.save(user);
        } catch (DuplicateKeyException e) {
            throw new RuntimeException("工号已存在，请使用其他工号");
        }
    }

    @Override
    public LoginResponse login(String username, String password) {
        if (!PasswordValidator.isValid(password)) {
            throw new RuntimeException("密码格式错误");
        }
        
        LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(User::getUsername, username);
        User user = this.getOne(wrapper);
        if (user == null) {
            throw new RuntimeException("工号不存在，请先注册");
        }
        if (user.getStatus() != 1) {
            throw new RuntimeException("账号已被禁用，请联系管理员");
        }
        if (!passwordUtil.matches(password, user.getPassword())) {
            throw new RuntimeException("密码错误，请重新输入");
        }
        String token = jwtUtil.generateToken(user.getId(), user.getUsername(), user.getRole());
        return new LoginResponse(token, user.getId(), user.getUsername(), user.getRole());
    }

}