package com.school.school_management.utils;

public class PasswordValidator {
    
    private static final String DIGIT = ".*[0-9].*";
    private static final String UPPERCASE = ".*[A-Z].*";
    private static final String LOWERCASE = ".*[a-z].*";
    private static final String SPECIAL_CHAR = ".*[^a-zA-Z0-9].*";
    
    public static boolean isValid(String password) {
        if (password == null || password.length() < 8 || password.length() > 20) {
            return false;
        }
        
        if (password.contains(" ")) {
            return false;
        }
        
        return password.matches(DIGIT) && 
               password.matches(UPPERCASE) && 
               password.matches(LOWERCASE) && 
               password.matches(SPECIAL_CHAR);
    }
    
    public static String getValidationMessage(String password) {
        if (password == null) {
            return "密码不能为空";
        }
        if (password.length() < 8 || password.length() > 20) {
            return "密码长度必须为8-20位";
        }
        if (password.contains(" ")) {
            return "密码不能包含空格";
        }
        
        StringBuilder missing = new StringBuilder();
        
        if (!password.matches(DIGIT)) {
            missing.append("数字");
        }
        if (!password.matches(UPPERCASE)) {
            if (missing.length() > 0) missing.append("、大写字母");
            else missing.append("大写字母");
        }
        if (!password.matches(LOWERCASE)) {
            if (missing.length() > 0) missing.append("、小写字母");
            else missing.append("小写字母");
        }
        if (!password.matches(SPECIAL_CHAR)) {
            if (missing.length() > 0) missing.append("、特殊符号");
            else missing.append("特殊符号");
        }
        
        if (missing.length() == 0) {
            return "密码格式正确";
        }
        
        return "密码必须包含：数字、大写字母、小写字母、特殊符号，当前缺少：" + missing.toString();
    }
}