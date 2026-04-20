package com.school.school_management.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.school.school_management.entity.User;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface UserMapper extends BaseMapper<User> {
}