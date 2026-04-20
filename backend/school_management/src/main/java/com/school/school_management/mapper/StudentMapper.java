package com.school.school_management.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.school.school_management.entity.Student;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface StudentMapper extends BaseMapper<Student> {
}