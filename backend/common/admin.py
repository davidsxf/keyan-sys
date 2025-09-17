from import_export.admin import ImportExportModelAdmin

class EncodingAwareImportExportModelAdmin(ImportExportModelAdmin):
    # 重写import_data方法以处理不同编码的文件
    def import_data(self, request, import_form, *args, **kwargs):
        # 获取上传的文件
        import_file = import_form.cleaned_data['import_file']
        
        # 尝试使用多种编码读取文件
        encodings = ['utf-8', 'utf-8-sig', 'gbk', 'latin-1']
        dataset = None
        
        try:
            for encoding in encodings:
                try:
                    # 重新定位文件指针到开始位置
                    import_file.seek(0)
                    # 获取文件格式
                    file_format = import_form.cleaned_data['input_format']()
                    
                    if file_format.is_binary():
                        # 二进制格式（如Excel）直接使用原始内容
                        dataset = file_format.create_dataset(import_file.read())
                        break
                    else:
                        # 文本格式尝试不同编码
                        file_content = import_file.read().decode(encoding)
                        dataset = file_format.create_dataset(file_content)
                        break
                except UnicodeDecodeError:
                    # 当前编码失败，尝试下一个
                    continue
                except Exception as e:
                    # 其他错误也尝试下一个编码
                    continue
        except Exception:
            # 如果所有尝试都失败，使用默认处理
            import_file.seek(0)
            return super().import_data(request, import_form, *args, **kwargs)
        
        if dataset is not None:
            # 使用读取到的dataset继续导入过程
            import_form.cleaned_data['import_file'] = dataset
        else:
            # 所有编码都失败，使用默认处理
            import_file.seek(0)
        
        return super().import_data(request, import_form, *args, **kwargs)